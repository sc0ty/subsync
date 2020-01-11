maxDistInfo = _(
'''Max adjustement. Subtitle time will be changed no more than this value. Higher value will result in longer synchronization, but if you set this too low, synchronization will fail.''')

effortInfo = _(
'''How hard should I work to synchronize subtitles. Higher value will result with better synchronization, but it will take longer.''')

noLanguageSelectedQuestion = _(
'''Langauge selection is not mandatory, but could drastically improve synchronization accuracy.
Are you sure?''')


### SettingsWin ###

maxPointDistInfo = _(
'''Maximum acceptable synchronization error, in seconds. Synchronization points with error greater than this will be discarded.''')

minPointsNoInfo = _(
'''Minumum number of synchronization points. Should not be set too high because it could result with generating large number of false positives.''')

minWordLenInfo = _(
'''Minimum word length, in letters. Shorter words will not be used as synchronization points. Applies only to alphabet-based languages.''')

minWordSimInfo = _(
'''Minimum words similarity for synchronization points. Between 0.0 and 1.0.''')

minCorrelationInfo = _(
'''Minimum correlation factor, between 0.0 and 1.0. Used to determine synchronization result. If correlation factor is smaller than this, synchronization will fail.''')

minWordProbInfo = _(
'''Minimum speech recognition score, between 0.0 and 1.0. Words transcribed with smaller score will be rejected.''')

outTimeOffset = _(
'''Fix output subtitle timestamps by given offset, in seconds.''')

jobsNoInfo = _(
'''Number of concurrent synchronization threads.''')
