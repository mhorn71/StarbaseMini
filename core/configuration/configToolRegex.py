__author__ = 'mark'
'''
Regex for configTool text line edits.

'''

observatory_name = '^([a-zA-Z0-9\'., ])*$'
observatory_description = '^([a-zA-Z0-9\'.,/ \\-])*$'
observatory_email = '^.*$'
observatory_telephone = '^.*$'
observatory_url = '^.*$'
observatory_country = '^[A-Z][A-Z]$'
observatory_timezone = '^.*$'
observatory_datum = '^(WGS84)|(EGM96)$'
observatory_geomag_model = '^.*$'
observatory_geomag_latitude = '^.*$'
observatory_geomag_longitude = '^.*$'
observatory_latitude = '^.*$'
observatory_longitude = '^.*$'
observatory_hasl = '^.*$'

observer_name = '^([a-zA-Z0-9\'., ])*$'
observer_description = '^([a-zA-Z0-9\'.,/ \\-])*$'
observer_email = '^.*$'
observer_telephone = '^.*$'
observer_url = '^.*$'
observer_country = '^[A-Z][A-Z]$'
observer_notes = '^([a-zA-Z0-9\'.,/ \\-])*$'

staribus_port = '^.*$'

starinet_ip = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
starinet_port = '^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$'

windows_path = '^.*$'
unix_path = '^.*$'