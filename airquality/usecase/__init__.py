# ======================================
# @author:  Davide Colombo
# @date:    2022-01-25, mar, 11:14
# ======================================

symbols = ['°', '#', '/', '$', ';', '=', '@']
MESSAGE_HEADER = ''.join(''.join(s for s in symbols) for _ in range(5))
START_MESSAGE = '%s STARTING NEW RUN %s' % (MESSAGE_HEADER, MESSAGE_HEADER)
END_MESSAGE = '%s END OF THE RUN %s' % (MESSAGE_HEADER, MESSAGE_HEADER)
