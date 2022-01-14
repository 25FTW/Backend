#   NO OUTPUT JUST FOR REFERENCE..........


datatable = """CREATE TABLE IF NOT EXISTS data (
username text NOT NULL PRIMARY KEY,category text, actual_item text, cost text, date text,
FOREIGN KEY (username) REFERENCES registerTable (username));
"""
