from datetime import datetime
# STRM is a unique property used by the HKU courses api, used to signify the current year and semester

# Calculate curret STRM
def calculate_strm():
  flag = "4"
  current_date = datetime.now().date()
  year = current_date.year
  month = current_date.month
  strms = []
  if month < 7:
    strms.append(flag + str(year - 1)[2:4] + '1')
    strms.append(flag + str(year - 1)[2:4] + '2')
    strms.append(flag + str(year - 1)[2:4] + '8')
  else:
    strms.append(flag + str(year)[2:-1] + '1')
    strms.append(flag + str(year)[2:-1] + '2')
    strms.append(flag + str(year)[2:-1] + '8')
  return strms

# Decode a given STRM into a year 
def decode_strm(strm : str):
  year = "20" + strm[1:3] + "-" + str(int(strm[1:3]) + 1)
  semester = strm[-1]
  semester = "Summer" if semester == '8' else semester
  return [year, semester]