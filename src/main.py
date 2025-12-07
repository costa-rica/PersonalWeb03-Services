"""
PersonalWeb03-Services main entry point.

This script serves as the entry point for all services in the PersonalWeb03-Services project.
Services can be run individually using command-line flags.
"""

import sys
import argparse
import logging
import json
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.config import Config
from utils.guardrail import TimeGuardrail
from services.left_off.onedrive_client import OneDriveClient
from services.left_off.document_parser import DocumentParser
from services.left_off.summarizer import Summarizer


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def run_left_off_service():
    """
    Run the LEFT-OFF.docx download and summary service.
    
    Returns:
        int: Exit code (0=success, 1=error)
    """
    logger.info("Starting LEFT-OFF service")
    
    try:
        # Load and validate configuration
        config = Config()
        config.validate_left_off_config()
        
        # Step 1: Download LEFT-OFF.docx from OneDrive
        logger.info("Step 1: Downloading LEFT-OFF.docx from OneDrive")
        client = OneDriveClient(
            application_id=config.application_id,
            client_secret=config.client_secret,
            refresh_token=config.refresh_token
        )
        
        # Get access token
        if not client.get_access_token():
            logger.error("Failed to obtain access token")
            return 1
        
        # Download LEFT-OFF.docx file
        output_path = config.get_left_off_file_path()
        if not client.download_file(config.target_file_id, str(output_path)):
            logger.error("Failed to download LEFT-OFF.docx")
            return 1
        
        # Step 2: Parse document and extract last 7 days
        logger.info("Step 2: Parsing document and extracting last 7 days")
        parser = DocumentParser(str(output_path))
        
        if not parser.load_document():
            logger.error("Failed to load document")
            return 1
        
        activities_path = config.get_activities_file_path()
        if not parser.extract_last_7_days(str(activities_path)):
            logger.error("Failed to extract last 7 days")
            return 1
        
        # Step 3: Generate AI-powered summary
        logger.info("Step 3: Generating AI-powered summary")
        template_path = Path(__file__).parent / 'templates' / 'left-off-summarizer.md'
        
        summarizer = Summarizer(
            api_key=config.openai_api_key,
            base_url=config.openai_base_url if config.openai_base_url != 'https://api.openai.com/v1' else None
        )
        
        summary_result = summarizer.generate_summary(
            str(activities_path),
            str(template_path)
        )
        
        if not summary_result:
            logger.error("Failed to generate summary")
            return 1
        
        # Save the JSON result to file
        summary_json_path = config.get_summary_json_path()
        try:
            with open(summary_json_path, 'w', encoding='utf-8') as f:
                json.dump(summary_result, f, indent=2)
            logger.info(f"Summary saved to: {summary_json_path}")
        except Exception as e:
            logger.error(f"Failed to save summary to file: {e}")
            return 1
        
        # Print the JSON result
        print("\n" + "="*80)
        print("SUMMARY RESULT:")
        print("="*80)
        print(json.dumps(summary_result, indent=2))
        print("="*80 + "\n")
        
        logger.info("LEFT-OFF service completed successfully")
        return 0
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='PersonalWeb03-Services - Run various services for PersonalWeb03'
    )
    
    parser.add_argument(
        '--run-left-off',
        action='store_true',
        help='Run the LEFT-OFF.docx download and summary service'
    )
    
    parser.add_argument(
        '--run-toggl',
        action='store_true',
        help='Run the Toggl Tracker to CSV service (not yet implemented)'
    )
    
    parser.add_argument(
        '--run-anyway',
        action='store_true',
        help='Bypass time window restrictions and run services at any time'
    )
    
    args = parser.parse_args()
    
    # If no service flag is specified, check time guardrail
    if not args.run_left_off and not args.run_toggl:
        logger.info("No service specified - checking time window guardrail")
        exit_code = TimeGuardrail.enforce(bypass=args.run_anyway)
        if exit_code != 0:
            sys.exit(exit_code)
        
        # If we get here, we're in the allowed window but no service was specified
        logger.info("Time window check passed, but no service was specified")
        parser.print_help()
        sys.exit(0)
    
    # Run the requested service (individual service flags can run anytime)
    if args.run_left_off:
        exit_code = run_left_off_service()
        sys.exit(exit_code)
    elif args.run_toggl:
        logger.error("Toggl service not yet implemented")
        sys.exit(1)


if __name__ == '__main__':
    main()
