# x_collector CLI without reply fetching (fast mode). usage: python _noreply_cli.py <same args as x_collector.py>
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import x_collector

async def _no_replies(*a, **k):
    return []

x_collector.fetch_x_replies = _no_replies
x_collector.main_cli()
