"""
Time-based guardrail for controlling service execution.
"""

import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class TimeGuardrail:
    """Enforces time-based execution windows for services."""
    
    # Allowed execution window
    ALLOWED_DAY = 6  # Sunday (0=Monday, 6=Sunday)
    ALLOWED_HOUR = 23  # 11 PM
    ALLOWED_MINUTE_START = 55  # 10:55 PM
    ALLOWED_MINUTE_END = 5  # 11:05 PM (5 minutes after)
    
    @classmethod
    def check_time_window(cls):
        """
        Check if current time is within the allowed execution window.
        
        Returns:
            bool: True if within allowed window, False otherwise
        """
        now = datetime.now()
        
        # Check if it's Sunday
        if now.weekday() != cls.ALLOWED_DAY:
            logger.warning(
                f"Execution blocked: Current day is {now.strftime('%A')}. "
                f"Services can only run on Sunday."
            )
            logger.warning(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.warning("Allowed window: Sunday 10:55 PM - 11:05 PM")
            return False
        
        # Check if it's within the time window (10:55 PM - 11:05 PM)
        current_hour = now.hour
        current_minute = now.minute
        
        # Check if we're in the 11 PM hour
        if current_hour == cls.ALLOWED_HOUR:
            # Between 10:55 PM and 11:05 PM
            if cls.ALLOWED_MINUTE_START <= current_minute <= 59 or current_minute <= cls.ALLOWED_MINUTE_END:
                logger.info("Time window check passed")
                return True
        
        # Outside allowed window
        logger.warning(
            f"Execution blocked: Current time is {now.strftime('%H:%M:%S')}. "
            f"Services can only run between 10:55 PM and 11:05 PM on Sunday."
        )
        logger.warning(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.warning("Allowed window: Sunday 10:55 PM - 11:05 PM")
        return False
    
    @classmethod
    def enforce(cls, bypass=False):
        """
        Enforce the time guardrail.
        
        Args:
            bypass: If True, bypass the time check
            
        Returns:
            int: 0 if allowed to proceed, 2 if blocked by time restriction
        """
        if bypass:
            logger.info("Time guardrail bypassed with --run-anyway flag")
            return 0
        
        if not cls.check_time_window():
            logger.error("Exiting due to time window restriction (exit code 2)")
            logger.info("Use --run-anyway flag to bypass time restrictions")
            return 2
        
        return 0
