def breakdowncalculator(df, chooseMRTline,stationFrom, stationTo):
    dfline = df[df['Line']==chooseMRTline]
    dfstationFr = dfline[dfline['Station Name']== stationFrom] ###### ask
    dfstationTo = dfline[dfline['Station Name']==stationTo]
    indexFr = int(dfstationFr['ind'])
    indexTo = int(dfstationTo['ind'])
    #print(indexFr, indexTo)

    # to get all the indexes between index from and index to
    if indexFr > indexTo:
        listFrTo = []
        for i in range(indexTo,indexFr + 1 ):
            listFrTo.append(i)
            #print(i)
    elif indexFr < indexTo:
        listFrTo = []
        for i in range(indexFr, indexTo + 1 ):
            listFrTo.append(i)
            #print(i)
    else :
        listFrTo = indexFr
        #print(listFrTo)

    # use the indexes to draw out the 
    dfPerFrTo = df[df['ind'].isin(listFrTo)]
    dfSumPerFrTo = sum(dfPerFrTo['Percentage'])
    return(dfSumPerFrTo)