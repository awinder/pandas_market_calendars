import pandas as pd 
import numpy as np 
from datetime import time 
from pytz import timezone 
from pandas_market_calendars.exchange_calendar_iex import IEXExchangeCalendar
from pandas_market_calendars.class_registry import _ProtectedDict 

iex = IEXExchangeCalendar()

def test_time_zone():
    assert iex.tz == timezone("America/New_York")
    assert iex.name == "IEX"


def test_open_close():
    assert iex.open_time == time(9, 30, tzinfo=timezone('America/New_York'))
    assert iex.close_time == time(16, tzinfo=timezone('America/New_York'))


def test_calendar_utility():
    assert len(iex.holidays().holidays) > 0
    assert isinstance(iex.regular_market_times, _ProtectedDict)
    
    valid_days = iex.valid_days(start_date='2016-12-20', end_date='2017-01-10')
    assert isinstance(valid_days, pd.DatetimeIndex)
    assert not valid_days.empty

    schedule = iex.schedule(start_date='2015-07-01', end_date='2017-07-10', start="pre", end="post")
    assert isinstance(schedule, pd.DataFrame)
    assert not schedule.empty


def test_trading_days_before_operation():
    trading_days = iex.valid_days(start_date="2000-01-01", end_date="2022-02-23")
    assert np.array([~(trading_days <= '2013-08-25')]).any()
