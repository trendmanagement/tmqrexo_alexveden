import pandas as pd

EXO_POS_DICT_TEST = {
    "transactions" : [
        {
            "date" : pd.Timestamp("2011-06-01T12:45:00"),
            "usdvalue" : 436.872556935259,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1112900",
                "dbid" : 14975,
                "hash" : 200014975
            },
            "qty" : 1.0,
            "price" : 8.73745113870518
        },
        {
            "date" : pd.Timestamp("2011-06-01T12:45:00"),
            "usdvalue" : 65737.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM11",
                "dbid" : 725,
                "hash" : 100000725
            },
            "qty" : 1.0,
            "price" : 1314.75
        },
        {
            "date" : pd.Timestamp("2011-06-01T12:45:00"),
            "usdvalue" : -258.951959638375,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1113400",
                "dbid" : 13955,
                "hash" : 200013955
            },
            "qty" : -1.0,
            "price" : 5.1790391927675
        },
        {
            "date" : pd.Timestamp("2011-06-01T12:45:00"),
            "usdvalue" : 61.0539140218144,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1113600",
                "dbid" : 14221,
                "hash" : 200014221
            },
            "qty" : 1.0,
            "price" : 1.22107828043629
        },
        {
            "date" : pd.Timestamp("2011-06-15T12:45:00"),
            "usdvalue" : -1136.66155373407,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1112900",
                "dbid" : 14975,
                "hash" : 200014975
            },
            "qty" : -1.0,
            "price" : 22.7332310746815
        },
        {
            "date" : pd.Timestamp("2011-06-15T12:45:00"),
            "usdvalue" : 0.00714017053089766,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1113400",
                "dbid" : 13955,
                "hash" : 200013955
            },
            "qty" : 1.0,
            "price" : 0.000142803410617953
        },
        {
            "date" : pd.Timestamp("2011-06-15T12:45:00"),
            "usdvalue" : -63387.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM11",
                "dbid" : 725,
                "hash" : 100000725
            },
            "qty" : -1.0,
            "price" : 1267.75
        },
        {
            "date" : pd.Timestamp("2011-06-15T12:45:00"),
            "usdvalue" : -0.00503657265657521,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1113600",
                "dbid" : 14221,
                "hash" : 200014221
            },
            "qty" : -1.0,
            "price" : 0.000100731453131504
        },
        {
            "date" : pd.Timestamp("2011-06-15T12:45:00"),
            "usdvalue" : 799.083994413473,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1112350",
                "dbid" : 1985000,
                "hash" : 201985000
            },
            "qty" : 1.0,
            "price" : 15.9816798882695
        },
        {
            "date" : pd.Timestamp("2011-06-15T12:45:00"),
            "usdvalue" : 63112.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU11",
                "dbid" : 749,
                "hash" : 100000749
            },
            "qty" : 1.0,
            "price" : 1262.25
        },
        {
            "date" : pd.Timestamp("2011-06-15T12:45:00"),
            "usdvalue" : -679.537300949238,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1112850",
                "dbid" : 1984963,
                "hash" : 201984963
            },
            "qty" : -1.0,
            "price" : 13.5907460189848
        },
        {
            "date" : pd.Timestamp("2011-06-15T12:45:00"),
            "usdvalue" : 334.391610938229,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1113050",
                "dbid" : 1984965,
                "hash" : 201984965
            },
            "qty" : 1.0,
            "price" : 6.68783221876458
        },
        {
            "date" : pd.Timestamp("2011-07-13T12:45:00"),
            "usdvalue" : -9.17955855235615,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1112350",
                "dbid" : 1985000,
                "hash" : 201985000
            },
            "qty" : -1.0,
            "price" : 0.183591171047123
        },
        {
            "date" : pd.Timestamp("2011-07-13T12:45:00"),
            "usdvalue" : 1451.50556450247,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1112850",
                "dbid" : 1984963,
                "hash" : 201984963
            },
            "qty" : 1.0,
            "price" : 29.0301112900495
        },
        {
            "date" : pd.Timestamp("2011-07-13T12:45:00"),
            "usdvalue" : -650.298126479913,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1113050",
                "dbid" : 1984965,
                "hash" : 201984965
            },
            "qty" : -1.0,
            "price" : 13.0059625295983
        },
        {
            "date" : pd.Timestamp("2011-07-13T12:45:00"),
            "usdvalue" : -65600.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU11",
                "dbid" : 749,
                "hash" : 100000749
            },
            "qty" : -1.0,
            "price" : 1312.0
        },
        {
            "date" : pd.Timestamp("2011-07-13T12:45:00"),
            "usdvalue" : 1026.331550912,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1112850",
                "dbid" : 2736667,
                "hash" : 202736667
            },
            "qty" : 1.0,
            "price" : 20.5266310182401
        },
        {
            "date" : pd.Timestamp("2011-07-13T12:45:00"),
            "usdvalue" : 65600.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU11",
                "dbid" : 749,
                "hash" : 100000749
            },
            "qty" : 1.0,
            "price" : 1312.0
        },
        {
            "date" : pd.Timestamp("2011-07-13T12:45:00"),
            "usdvalue" : -872.013606402237,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1113350",
                "dbid" : 2736526,
                "hash" : 202736526
            },
            "qty" : -1.0,
            "price" : 17.4402721280447
        },
        {
            "date" : pd.Timestamp("2011-07-13T12:45:00"),
            "usdvalue" : 492.950012050218,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1113550",
                "dbid" : 2736530,
                "hash" : 202736530
            },
            "qty" : 1.0,
            "price" : 9.85900024100437
        },
        {
            "date" : pd.Timestamp("2011-08-17T12:45:00"),
            "usdvalue" : -0.191843439539149,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1113550",
                "dbid" : 2736530,
                "hash" : 202736530
            },
            "qty" : -1.0,
            "price" : 0.00383686879078299
        },
        {
            "date" : pd.Timestamp("2011-08-17T12:45:00"),
            "usdvalue" : -4711.36042957972,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1112850",
                "dbid" : 2736667,
                "hash" : 202736667
            },
            "qty" : -1.0,
            "price" : 94.2272085915945
        },
        {
            "date" : pd.Timestamp("2011-08-17T12:45:00"),
            "usdvalue" : -59537.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU11",
                "dbid" : 749,
                "hash" : 100000749
            },
            "qty" : -1.0,
            "price" : 1190.75
        },
        {
            "date" : pd.Timestamp("2011-08-17T12:45:00"),
            "usdvalue" : 0.198109603833413,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1113350",
                "dbid" : 2736526,
                "hash" : 202736526
            },
            "qty" : 1.0,
            "price" : 0.00396219207666826
        },
        {
            "date" : pd.Timestamp("2011-08-17T12:45:00"),
            "usdvalue" : 1481.79807872996,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1111650",
                "dbid" : 1985013,
                "hash" : 201985013
            },
            "qty" : 1.0,
            "price" : 29.6359615745992
        },
        {
            "date" : pd.Timestamp("2011-08-17T12:45:00"),
            "usdvalue" : 59537.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU11",
                "dbid" : 749,
                "hash" : 100000749
            },
            "qty" : 1.0,
            "price" : 1190.75
        },
        {
            "date" : pd.Timestamp("2011-08-17T12:45:00"),
            "usdvalue" : -1278.53872438702,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1112150",
                "dbid" : 1984975,
                "hash" : 201984975
            },
            "qty" : -1.0,
            "price" : 25.5707744877404
        },
        {
            "date" : pd.Timestamp("2011-08-17T12:45:00"),
            "usdvalue" : 844.72507954849,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1112350",
                "dbid" : 1984976,
                "hash" : 201984976
            },
            "qty" : 1.0,
            "price" : 16.8945015909698
        },
        {
            "date" : pd.Timestamp("2011-09-14T12:45:00"),
            "usdvalue" : -55.3910707701412,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1112350",
                "dbid" : 1984976,
                "hash" : 201984976
            },
            "qty" : -1.0,
            "price" : 1.10782141540282
        },
        {
            "date" : pd.Timestamp("2011-09-14T12:45:00"),
            "usdvalue" : -59787.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU11",
                "dbid" : 749,
                "hash" : 100000749
            },
            "qty" : -1.0,
            "price" : 1195.75
        },
        {
            "date" : pd.Timestamp("2011-09-14T12:45:00"),
            "usdvalue" : -118.534776114757,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1111650",
                "dbid" : 1985013,
                "hash" : 201985013
            },
            "qty" : -1.0,
            "price" : 2.37069552229514
        },
        {
            "date" : pd.Timestamp("2011-09-14T12:45:00"),
            "usdvalue" : 193.234132962718,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1112150",
                "dbid" : 1984975,
                "hash" : 201984975
            },
            "qty" : 1.0,
            "price" : 3.86468265925436
        },
        {
            "date" : pd.Timestamp("2011-09-14T12:45:00"),
            "usdvalue" : 1934.56643854564,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1111650",
                "dbid" : 4402343,
                "hash" : 204402343
            },
            "qty" : 1.0,
            "price" : 38.6913287709128
        },
        {
            "date" : pd.Timestamp("2011-09-14T12:45:00"),
            "usdvalue" : 59462.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ11",
                "dbid" : 758,
                "hash" : 100000758
            },
            "qty" : 1.0,
            "price" : 1189.25
        },
        {
            "date" : pd.Timestamp("2011-09-14T12:45:00"),
            "usdvalue" : -1690.05448462206,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1112150",
                "dbid" : 4402244,
                "hash" : 204402244
            },
            "qty" : -1.0,
            "price" : 33.8010896924411
        },
        {
            "date" : pd.Timestamp("2011-09-14T12:45:00"),
            "usdvalue" : 1241.24605781939,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1112350",
                "dbid" : 4402245,
                "hash" : 204402245
            },
            "qty" : 1.0,
            "price" : 24.8249211563877
        },
        {
            "date" : pd.Timestamp("2011-10-19T12:45:00"),
            "usdvalue" : 413.832939004723,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1112150",
                "dbid" : 4402244,
                "hash" : 204402244
            },
            "qty" : 1.0,
            "price" : 8.27665878009446
        },
        {
            "date" : pd.Timestamp("2011-10-19T12:45:00"),
            "usdvalue" : -114.778180643613,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1112350",
                "dbid" : 4402245,
                "hash" : 204402245
            },
            "qty" : -1.0,
            "price" : 2.29556361287226
        },
        {
            "date" : pd.Timestamp("2011-10-19T12:45:00"),
            "usdvalue" : -60312.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ11",
                "dbid" : 758,
                "hash" : 100000758
            },
            "qty" : -1.0,
            "price" : 1206.25
        },
        {
            "date" : pd.Timestamp("2011-10-19T12:45:00"),
            "usdvalue" : -135.519607052278,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1111650",
                "dbid" : 4402343,
                "hash" : 204402343
            },
            "qty" : -1.0,
            "price" : 2.71039214104556
        },
        {
            "date" : pd.Timestamp("2011-10-19T12:45:00"),
            "usdvalue" : 1480.49731022301,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1111800",
                "dbid" : 5126381,
                "hash" : 205126381
            },
            "qty" : 1.0,
            "price" : 29.6099462044601
        },
        {
            "date" : pd.Timestamp("2011-10-19T12:45:00"),
            "usdvalue" : 60312.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ11",
                "dbid" : 758,
                "hash" : 100000758
            },
            "qty" : 1.0,
            "price" : 1206.25
        },
        {
            "date" : pd.Timestamp("2011-10-19T12:45:00"),
            "usdvalue" : -1294.6646540407,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1112300",
                "dbid" : 5126234,
                "hash" : 205126234
            },
            "qty" : -1.0,
            "price" : 25.8932930808139
        },
        {
            "date" : pd.Timestamp("2011-10-19T12:45:00"),
            "usdvalue" : 846.920560976665,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1112500",
                "dbid" : 5126236,
                "hash" : 205126236
            },
            "qty" : 1.0,
            "price" : 16.9384112195333
        },
        {
            "date" : pd.Timestamp("2011-11-16T12:45:00"),
            "usdvalue" : 901.580783249835,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1112300",
                "dbid" : 5126234,
                "hash" : 205126234
            },
            "qty" : 1.0,
            "price" : 18.0316156649967
        },
        {
            "date" : pd.Timestamp("2011-11-16T12:45:00"),
            "usdvalue" : -353.053365449574,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1112500",
                "dbid" : 5126236,
                "hash" : 205126236
            },
            "qty" : -1.0,
            "price" : 7.06106730899148
        },
        {
            "date" : pd.Timestamp("2011-11-16T12:45:00"),
            "usdvalue" : -67.3610068182803,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1111800",
                "dbid" : 5126381,
                "hash" : 205126381
            },
            "qty" : -1.0,
            "price" : 1.34722013636561
        },
        {
            "date" : pd.Timestamp("2011-11-16T12:45:00"),
            "usdvalue" : -61975.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ11",
                "dbid" : 758,
                "hash" : 100000758
            },
            "qty" : -1.0,
            "price" : 1239.5
        },
        {
            "date" : pd.Timestamp("2011-11-16T12:45:00"),
            "usdvalue" : 1538.34535274291,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1112150",
                "dbid" : 4402321,
                "hash" : 204402321
            },
            "qty" : 1.0,
            "price" : 30.7669070548582
        },
        {
            "date" : pd.Timestamp("2011-11-16T12:45:00"),
            "usdvalue" : 61975.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ11",
                "dbid" : 758,
                "hash" : 100000758
            },
            "qty" : 1.0,
            "price" : 1239.5
        },
        {
            "date" : pd.Timestamp("2011-11-16T12:45:00"),
            "usdvalue" : -1298.05547114868,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1112650",
                "dbid" : 4168208,
                "hash" : 204168208
            },
            "qty" : -1.0,
            "price" : 25.9611094229737
        },
        {
            "date" : pd.Timestamp("2011-11-16T12:45:00"),
            "usdvalue" : 862.396286199942,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1112850",
                "dbid" : 4402283,
                "hash" : 204402283
            },
            "qty" : 1.0,
            "price" : 17.2479257239988
        },
        {
            "date" : pd.Timestamp("2011-12-14T12:45:00"),
            "usdvalue" : 2.40604334342187,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1112650",
                "dbid" : 4168208,
                "hash" : 204168208
            },
            "qty" : 1.0,
            "price" : 0.0481208668684374
        },
        {
            "date" : pd.Timestamp("2011-12-14T12:45:00"),
            "usdvalue" : -553.160733511555,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1112150",
                "dbid" : 4402321,
                "hash" : 204402321
            },
            "qty" : -1.0,
            "price" : 11.0632146702311
        },
        {
            "date" : pd.Timestamp("2011-12-14T12:45:00"),
            "usdvalue" : -0.242375199306438,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1112850",
                "dbid" : 4402283,
                "hash" : 204402283
            },
            "qty" : -1.0,
            "price" : 0.00484750398612876
        },
        {
            "date" : pd.Timestamp("2011-12-14T12:45:00"),
            "usdvalue" : -60600.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ11",
                "dbid" : 758,
                "hash" : 100000758
            },
            "qty" : -1.0,
            "price" : 1212.0
        },
        {
            "date" : pd.Timestamp("2011-12-14T12:45:00"),
            "usdvalue" : 1452.40654621938,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1211800",
                "dbid" : 11508779,
                "hash" : 211508779
            },
            "qty" : 1.0,
            "price" : 29.0481309243876
        },
        {
            "date" : pd.Timestamp("2011-12-14T12:45:00"),
            "usdvalue" : 60300.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH12",
                "dbid" : 759,
                "hash" : 100000759
            },
            "qty" : 1.0,
            "price" : 1206.0
        },
        {
            "date" : pd.Timestamp("2011-12-14T12:45:00"),
            "usdvalue" : -1299.31047978881,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1212300",
                "dbid" : 11508656,
                "hash" : 211508656
            },
            "qty" : -1.0,
            "price" : 25.9862095957762
        },
        {
            "date" : pd.Timestamp("2011-12-14T12:45:00"),
            "usdvalue" : 871.498524718402,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1212500",
                "dbid" : 11508658,
                "hash" : 211508658
            },
            "qty" : 1.0,
            "price" : 17.429970494368
        },
        {
            "date" : pd.Timestamp("2012-01-18T12:45:00"),
            "usdvalue" : 3628.62091746658,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1212300",
                "dbid" : 11508656,
                "hash" : 211508656
            },
            "qty" : 1.0,
            "price" : 72.5724183493317
        },
        {
            "date" : pd.Timestamp("2012-01-18T12:45:00"),
            "usdvalue" : -2632.16999998311,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1212500",
                "dbid" : 11508658,
                "hash" : 211508658
            },
            "qty" : -1.0,
            "price" : 52.6433999996623
        },
        {
            "date" : pd.Timestamp("2012-01-18T12:45:00"),
            "usdvalue" : -1.07696171213159,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1211800",
                "dbid" : 11508779,
                "hash" : 211508779
            },
            "qty" : -1.0,
            "price" : 0.0215392342426317
        },
        {
            "date" : pd.Timestamp("2012-01-18T12:45:00"),
            "usdvalue" : -65125.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH12",
                "dbid" : 759,
                "hash" : 100000759
            },
            "qty" : -1.0,
            "price" : 1302.5
        },
        {
            "date" : pd.Timestamp("2012-01-18T12:45:00"),
            "usdvalue" : 907.263965439569,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1212750",
                "dbid" : 11520147,
                "hash" : 211520147
            },
            "qty" : 1.0,
            "price" : 18.1452793087914
        },
        {
            "date" : pd.Timestamp("2012-01-18T12:45:00"),
            "usdvalue" : 65125.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH12",
                "dbid" : 759,
                "hash" : 100000759
            },
            "qty" : 1.0,
            "price" : 1302.5
        },
        {
            "date" : pd.Timestamp("2012-01-18T12:45:00"),
            "usdvalue" : -776.751524121252,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1213250",
                "dbid" : 11519994,
                "hash" : 211519994
            },
            "qty" : -1.0,
            "price" : 15.535030482425
        },
        {
            "date" : pd.Timestamp("2012-01-18T12:45:00"),
            "usdvalue" : 429.190541174628,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1213450",
                "dbid" : 11519998,
                "hash" : 211519998
            },
            "qty" : 1.0,
            "price" : 8.58381082349257
        },
        {
            "date" : pd.Timestamp("2012-02-15T12:45:00"),
            "usdvalue" : 962.983561001226,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1213250",
                "dbid" : 11519994,
                "hash" : 211519994
            },
            "qty" : 1.0,
            "price" : 19.2596712200245
        },
        {
            "date" : pd.Timestamp("2012-02-15T12:45:00"),
            "usdvalue" : -6.90031230279882,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1212750",
                "dbid" : 11520147,
                "hash" : 211520147
            },
            "qty" : -1.0,
            "price" : 0.138006246055976
        },
        {
            "date" : pd.Timestamp("2012-02-15T12:45:00"),
            "usdvalue" : -248.314467612494,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1213450",
                "dbid" : 11519998,
                "hash" : 211519998
            },
            "qty" : -1.0,
            "price" : 4.96628935224987
        },
        {
            "date" : pd.Timestamp("2012-02-15T12:45:00"),
            "usdvalue" : -67112.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH12",
                "dbid" : 759,
                "hash" : 100000759
            },
            "qty" : -1.0,
            "price" : 1342.25
        },
        {
            "date" : pd.Timestamp("2012-02-15T12:45:00"),
            "usdvalue" : 832.670319592916,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1213150",
                "dbid" : 11512487,
                "hash" : 211512487
            },
            "qty" : 1.0,
            "price" : 16.6534063918583
        },
        {
            "date" : pd.Timestamp("2012-02-15T12:45:00"),
            "usdvalue" : 67112.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH12",
                "dbid" : 759,
                "hash" : 100000759
            },
            "qty" : 1.0,
            "price" : 1342.25
        },
        {
            "date" : pd.Timestamp("2012-02-15T12:45:00"),
            "usdvalue" : -683.760930539378,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1213650",
                "dbid" : 11520725,
                "hash" : 211520725
            },
            "qty" : -1.0,
            "price" : 13.6752186107876
        },
        {
            "date" : pd.Timestamp("2012-02-15T12:45:00"),
            "usdvalue" : 326.46086838995,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1213850",
                "dbid" : 11520726,
                "hash" : 211520726
            },
            "qty" : 1.0,
            "price" : 6.52921736779899
        },
        {
            "date" : pd.Timestamp("2012-03-14T12:45:00"),
            "usdvalue" : -5.05563985635842,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1213150",
                "dbid" : 11512487,
                "hash" : 211512487
            },
            "qty" : -1.0,
            "price" : 0.101112797127168
        },
        {
            "date" : pd.Timestamp("2012-03-14T12:45:00"),
            "usdvalue" : 1457.0148366918,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1213650",
                "dbid" : 11520725,
                "hash" : 211520725
            },
            "qty" : 1.0,
            "price" : 29.1402967338361
        },
        {
            "date" : pd.Timestamp("2012-03-14T12:45:00"),
            "usdvalue" : -564.136506462069,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1213850",
                "dbid" : 11520726,
                "hash" : 211520726
            },
            "qty" : -1.0,
            "price" : 11.2827301292414
        },
        {
            "date" : pd.Timestamp("2012-03-14T12:45:00"),
            "usdvalue" : -69675.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH12",
                "dbid" : 759,
                "hash" : 100000759
            },
            "qty" : -1.0,
            "price" : 1393.5
        },
        {
            "date" : pd.Timestamp("2012-03-14T12:45:00"),
            "usdvalue" : 844.956481978866,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1213650",
                "dbid" : 11528676,
                "hash" : 211528676
            },
            "qty" : 1.0,
            "price" : 16.8991296395773
        },
        {
            "date" : pd.Timestamp("2012-03-14T12:45:00"),
            "usdvalue" : 69387.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM12",
                "dbid" : 3100,
                "hash" : 100003100
            },
            "qty" : 1.0,
            "price" : 1387.75
        },
        {
            "date" : pd.Timestamp("2012-03-14T12:45:00"),
            "usdvalue" : -571.76151178752,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1214150",
                "dbid" : 11653100,
                "hash" : 211653100
            },
            "qty" : -1.0,
            "price" : 11.4352302357504
        },
        {
            "date" : pd.Timestamp("2012-03-14T12:45:00"),
            "usdvalue" : 284.133880079136,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1214350",
                "dbid" : 11653923,
                "hash" : 211653923
            },
            "qty" : 1.0,
            "price" : 5.68267760158272
        },
        {
            "date" : pd.Timestamp("2012-04-18T12:45:00"),
            "usdvalue" : -69125.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM12",
                "dbid" : 3100,
                "hash" : 100003100
            },
            "qty" : -1.0,
            "price" : 1382.5
        },
        {
            "date" : pd.Timestamp("2012-04-18T12:45:00"),
            "usdvalue" : -1.26854038602113,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1214350",
                "dbid" : 11653923,
                "hash" : 211653923
            },
            "qty" : -1.0,
            "price" : 0.0253708077204227
        },
        {
            "date" : pd.Timestamp("2012-04-18T12:45:00"),
            "usdvalue" : -121.485346097776,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1213650",
                "dbid" : 11528676,
                "hash" : 211528676
            },
            "qty" : -1.0,
            "price" : 2.42970692195553
        },
        {
            "date" : pd.Timestamp("2012-04-18T12:45:00"),
            "usdvalue" : 13.3709448565902,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1214150",
                "dbid" : 11653100,
                "hash" : 211653100
            },
            "qty" : 1.0,
            "price" : 0.267418897131805
        },
        {
            "date" : pd.Timestamp("2012-04-18T12:45:00"),
            "usdvalue" : 851.973271184275,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1213550",
                "dbid" : 11653465,
                "hash" : 211653465
            },
            "qty" : 1.0,
            "price" : 17.0394654236855
        },
        {
            "date" : pd.Timestamp("2012-04-18T12:45:00"),
            "usdvalue" : 69125.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM12",
                "dbid" : 3100,
                "hash" : 100003100
            },
            "qty" : 1.0,
            "price" : 1382.5
        },
        {
            "date" : pd.Timestamp("2012-04-18T12:45:00"),
            "usdvalue" : -720.898781121639,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1214050",
                "dbid" : 11653323,
                "hash" : 211653323
            },
            "qty" : -1.0,
            "price" : 14.4179756224328
        },
        {
            "date" : pd.Timestamp("2012-04-18T12:45:00"),
            "usdvalue" : 362.777044219703,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1214250",
                "dbid" : 11653327,
                "hash" : 211653327
            },
            "qty" : 1.0,
            "price" : 7.25554088439407
        },
        {
            "date" : pd.Timestamp("2012-05-16T12:45:00"),
            "usdvalue" : -1554.31983994176,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1213550",
                "dbid" : 11653465,
                "hash" : 211653465
            },
            "qty" : -1.0,
            "price" : 31.0863967988353
        },
        {
            "date" : pd.Timestamp("2012-05-16T12:45:00"),
            "usdvalue" : 0.171214903999589,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1214050",
                "dbid" : 11653323,
                "hash" : 211653323
            },
            "qty" : 1.0,
            "price" : 0.00342429807999178
        },
        {
            "date" : pd.Timestamp("2012-05-16T12:45:00"),
            "usdvalue" : -66225.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM12",
                "dbid" : 3100,
                "hash" : 100003100
            },
            "qty" : -1.0,
            "price" : 1324.5
        },
        {
            "date" : pd.Timestamp("2012-05-16T12:45:00"),
            "usdvalue" : -0.179638846358576,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1214250",
                "dbid" : 11653327,
                "hash" : 211653327
            },
            "qty" : -1.0,
            "price" : 0.00359277692717153
        },
        {
            "date" : pd.Timestamp("2012-05-16T12:45:00"),
            "usdvalue" : 1076.61713023246,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1213000",
                "dbid" : 4438948,
                "hash" : 204438948
            },
            "qty" : 1.0,
            "price" : 21.5323426046492
        },
        {
            "date" : pd.Timestamp("2012-05-16T12:45:00"),
            "usdvalue" : 66225.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM12",
                "dbid" : 3100,
                "hash" : 100003100
            },
            "qty" : 1.0,
            "price" : 1324.5
        },
        {
            "date" : pd.Timestamp("2012-05-16T12:45:00"),
            "usdvalue" : -852.383398701846,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1213500",
                "dbid" : 4438851,
                "hash" : 204438851
            },
            "qty" : -1.0,
            "price" : 17.0476679740369
        },
        {
            "date" : pd.Timestamp("2012-05-16T12:45:00"),
            "usdvalue" : 482.981618688498,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1213700",
                "dbid" : 4438810,
                "hash" : 204438810
            },
            "qty" : 1.0,
            "price" : 9.65963237376997
        },
        {
            "date" : pd.Timestamp("2012-06-13T12:45:00"),
            "usdvalue" : -165.259413460632,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1213000",
                "dbid" : 4438948,
                "hash" : 204438948
            },
            "qty" : -1.0,
            "price" : 3.30518826921264
        },
        {
            "date" : pd.Timestamp("2012-06-13T12:45:00"),
            "usdvalue" : -0.149473705317682,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1213700",
                "dbid" : 4438810,
                "hash" : 204438810
            },
            "qty" : -1.0,
            "price" : 0.00298947410635364
        },
        {
            "date" : pd.Timestamp("2012-06-13T12:45:00"),
            "usdvalue" : 2.08645340401823,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1213500",
                "dbid" : 4438851,
                "hash" : 204438851
            },
            "qty" : 1.0,
            "price" : 0.0417290680803646
        },
        {
            "date" : pd.Timestamp("2012-06-13T12:45:00"),
            "usdvalue" : -65625.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM12",
                "dbid" : 3100,
                "hash" : 100003100
            },
            "qty" : -1.0,
            "price" : 1312.5
        },
        {
            "date" : pd.Timestamp("2012-06-13T12:45:00"),
            "usdvalue" : 1302.08184444199,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1212800",
                "dbid" : 11657911,
                "hash" : 211657911
            },
            "qty" : 1.0,
            "price" : 26.0416368888398
        },
        {
            "date" : pd.Timestamp("2012-06-13T12:45:00"),
            "usdvalue" : 65287.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU12",
                "dbid" : 3099,
                "hash" : 100003099
            },
            "qty" : 1.0,
            "price" : 1305.75
        },
        {
            "date" : pd.Timestamp("2012-06-13T12:45:00"),
            "usdvalue" : -1112.02246306889,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1213300",
                "dbid" : 11657794,
                "hash" : 211657794
            },
            "qty" : -1.0,
            "price" : 22.2404492613779
        },
        {
            "date" : pd.Timestamp("2012-06-13T12:45:00"),
            "usdvalue" : 688.770960141312,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1213500",
                "dbid" : 11657796,
                "hash" : 211657796
            },
            "qty" : 1.0,
            "price" : 13.7754192028262
        },
        {
            "date" : pd.Timestamp("2012-07-18T12:45:00"),
            "usdvalue" : 1886.83154252022,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1213300",
                "dbid" : 11657794,
                "hash" : 211657794
            },
            "qty" : 1.0,
            "price" : 37.7366308504045
        },
        {
            "date" : pd.Timestamp("2012-07-18T12:45:00"),
            "usdvalue" : -68375.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU12",
                "dbid" : 3099,
                "hash" : 100003099
            },
            "qty" : -1.0,
            "price" : 1367.5
        },
        {
            "date" : pd.Timestamp("2012-07-18T12:45:00"),
            "usdvalue" : -934.469188949549,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1213500",
                "dbid" : 11657796,
                "hash" : 211657796
            },
            "qty" : -1.0,
            "price" : 18.689383778991
        },
        {
            "date" : pd.Timestamp("2012-07-18T12:45:00"),
            "usdvalue" : -1.36582558116181,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1212800",
                "dbid" : 11657911,
                "hash" : 211657911
            },
            "qty" : -1.0,
            "price" : 0.0273165116232361
        },
        {
            "date" : pd.Timestamp("2012-07-18T12:45:00"),
            "usdvalue" : 675.138304612011,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1213400",
                "dbid" : 11665497,
                "hash" : 211665497
            },
            "qty" : 1.0,
            "price" : 13.5027660922402
        },
        {
            "date" : pd.Timestamp("2012-07-18T12:45:00"),
            "usdvalue" : 68375.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU12",
                "dbid" : 3099,
                "hash" : 100003099
            },
            "qty" : 1.0,
            "price" : 1367.5
        },
        {
            "date" : pd.Timestamp("2012-07-18T12:45:00"),
            "usdvalue" : -591.558561409667,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1213900",
                "dbid" : 11665345,
                "hash" : 211665345
            },
            "qty" : -1.0,
            "price" : 11.8311712281933
        },
        {
            "date" : pd.Timestamp("2012-07-18T12:45:00"),
            "usdvalue" : 290.299795482505,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1214100",
                "dbid" : 11665349,
                "hash" : 211665349
            },
            "qty" : 1.0,
            "price" : 5.80599590965011
        },
        {
            "date" : pd.Timestamp("2012-08-15T12:45:00"),
            "usdvalue" : -2.77558243205345,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1213400",
                "dbid" : 11665497,
                "hash" : 211665497
            },
            "qty" : -1.0,
            "price" : 0.0555116486410689
        },
        {
            "date" : pd.Timestamp("2012-08-15T12:45:00"),
            "usdvalue" : -70187.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU12",
                "dbid" : 3099,
                "hash" : 100003099
            },
            "qty" : -1.0,
            "price" : 1403.75
        },
        {
            "date" : pd.Timestamp("2012-08-15T12:45:00"),
            "usdvalue" : -125.598957326676,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1214100",
                "dbid" : 11665349,
                "hash" : 211665349
            },
            "qty" : -1.0,
            "price" : 2.51197914653352
        },
        {
            "date" : pd.Timestamp("2012-08-15T12:45:00"),
            "usdvalue" : 762.699209025811,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1213900",
                "dbid" : 11665345,
                "hash" : 211665345
            },
            "qty" : 1.0,
            "price" : 15.2539841805162
        },
        {
            "date" : pd.Timestamp("2012-08-15T12:45:00"),
            "usdvalue" : 815.249927165425,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1213800",
                "dbid" : 11512822,
                "hash" : 211512822
            },
            "qty" : 1.0,
            "price" : 16.3049985433085
        },
        {
            "date" : pd.Timestamp("2012-08-15T12:45:00"),
            "usdvalue" : 70187.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU12",
                "dbid" : 3099,
                "hash" : 100003099
            },
            "qty" : 1.0,
            "price" : 1403.75
        },
        {
            "date" : pd.Timestamp("2012-08-15T12:45:00"),
            "usdvalue" : -606.400503125909,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1214300",
                "dbid" : 11512703,
                "hash" : 211512703
            },
            "qty" : -1.0,
            "price" : 12.1280100625182
        },
        {
            "date" : pd.Timestamp("2012-08-15T12:45:00"),
            "usdvalue" : 306.437784711429,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1214500",
                "dbid" : 11512705,
                "hash" : 211512705
            },
            "qty" : 1.0,
            "price" : 6.12875569422857
        },
        {
            "date" : pd.Timestamp("2012-09-19T12:45:00"),
            "usdvalue" : -702.527881489186,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1214500",
                "dbid" : 11512705,
                "hash" : 211512705
            },
            "qty" : -1.0,
            "price" : 14.0505576297837
        },
        {
            "date" : pd.Timestamp("2012-09-19T12:45:00"),
            "usdvalue" : -73162.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU12",
                "dbid" : 3099,
                "hash" : 100003099
            },
            "qty" : -1.0,
            "price" : 1463.25
        },
        {
            "date" : pd.Timestamp("2012-09-19T12:45:00"),
            "usdvalue" : -1.74962002100707,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1213800",
                "dbid" : 11512822,
                "hash" : 211512822
            },
            "qty" : -1.0,
            "price" : 0.0349924004201414
        },
        {
            "date" : pd.Timestamp("2012-09-19T12:45:00"),
            "usdvalue" : 1669.10518598639,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1214300",
                "dbid" : 11512703,
                "hash" : 211512703
            },
            "qty" : 1.0,
            "price" : 33.3821037197279
        },
        {
            "date" : pd.Timestamp("2012-09-19T12:45:00"),
            "usdvalue" : 571.847557130337,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1214300",
                "dbid" : 11667931,
                "hash" : 211667931
            },
            "qty" : 1.0,
            "price" : 11.4369511426067
        },
        {
            "date" : pd.Timestamp("2012-09-19T12:45:00"),
            "usdvalue" : 72837.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ12",
                "dbid" : 3408,
                "hash" : 100003408
            },
            "qty" : 1.0,
            "price" : 1456.75
        },
        {
            "date" : pd.Timestamp("2012-09-19T12:45:00"),
            "usdvalue" : -485.509796553717,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1214800",
                "dbid" : 11667791,
                "hash" : 211667791
            },
            "qty" : -1.0,
            "price" : 9.71019593107434
        },
        {
            "date" : pd.Timestamp("2012-09-19T12:45:00"),
            "usdvalue" : 221.029014296431,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1215000",
                "dbid" : 11667793,
                "hash" : 211667793
            },
            "qty" : 1.0,
            "price" : 4.42058028592862
        },
        {
            "date" : pd.Timestamp("2012-10-17T12:45:00"),
            "usdvalue" : -72825.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ12",
                "dbid" : 3408,
                "hash" : 100003408
            },
            "qty" : -1.0,
            "price" : 1456.5
        },
        {
            "date" : pd.Timestamp("2012-10-17T12:45:00"),
            "usdvalue" : -3.02770531851611,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1215000",
                "dbid" : 11667793,
                "hash" : 211667793
            },
            "qty" : -1.0,
            "price" : 0.0605541063703221
        },
        {
            "date" : pd.Timestamp("2012-10-17T12:45:00"),
            "usdvalue" : -22.8718855186003,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1214300",
                "dbid" : 11667931,
                "hash" : 211667931
            },
            "qty" : -1.0,
            "price" : 0.457437710372005
        },
        {
            "date" : pd.Timestamp("2012-10-17T12:45:00"),
            "usdvalue" : 16.3012919281989,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1214800",
                "dbid" : 11667791,
                "hash" : 211667791
            },
            "qty" : 1.0,
            "price" : 0.326025838563979
        },
        {
            "date" : pd.Timestamp("2012-10-17T12:45:00"),
            "usdvalue" : 641.904401177487,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1214300",
                "dbid" : 11673695,
                "hash" : 211673695
            },
            "qty" : 1.0,
            "price" : 12.8380880235497
        },
        {
            "date" : pd.Timestamp("2012-10-17T12:45:00"),
            "usdvalue" : 72825.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ12",
                "dbid" : 3408,
                "hash" : 100003408
            },
            "qty" : 1.0,
            "price" : 1456.5
        },
        {
            "date" : pd.Timestamp("2012-10-17T12:45:00"),
            "usdvalue" : -537.061137660487,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1214800",
                "dbid" : 11673540,
                "hash" : 211673540
            },
            "qty" : -1.0,
            "price" : 10.7412227532097
        },
        {
            "date" : pd.Timestamp("2012-10-17T12:45:00"),
            "usdvalue" : 253.859415988902,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1215000",
                "dbid" : 11673544,
                "hash" : 211673544
            },
            "qty" : 1.0,
            "price" : 5.07718831977803
        },
        {
            "date" : pd.Timestamp("2012-11-14T12:45:00"),
            "usdvalue" : -67675.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ12",
                "dbid" : 3408,
                "hash" : 100003408
            },
            "qty" : -1.0,
            "price" : 1353.5
        },
        {
            "date" : pd.Timestamp("2012-11-14T12:45:00"),
            "usdvalue" : -0.0358235998841744,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1215000",
                "dbid" : 11673544,
                "hash" : 211673544
            },
            "qty" : -1.0,
            "price" : 0.000716471997683488
        },
        {
            "date" : pd.Timestamp("2012-11-14T12:45:00"),
            "usdvalue" : 0.0332871051409812,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1214800",
                "dbid" : 11673540,
                "hash" : 211673540
            },
            "qty" : 1.0,
            "price" : 0.000665742102819625
        },
        {
            "date" : pd.Timestamp("2012-11-14T12:45:00"),
            "usdvalue" : -3823.87050804072,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1214300",
                "dbid" : 11673695,
                "hash" : 211673695
            },
            "qty" : -1.0,
            "price" : 76.4774101608143
        },
        {
            "date" : pd.Timestamp("2012-11-14T12:45:00"),
            "usdvalue" : 973.499916118695,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1213300",
                "dbid" : 11528015,
                "hash" : 211528015
            },
            "qty" : 1.0,
            "price" : 19.4699983223739
        },
        {
            "date" : pd.Timestamp("2012-11-14T12:45:00"),
            "usdvalue" : 67675.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ12",
                "dbid" : 3408,
                "hash" : 100003408
            },
            "qty" : 1.0,
            "price" : 1353.5
        },
        {
            "date" : pd.Timestamp("2012-11-14T12:45:00"),
            "usdvalue" : -773.210082643479,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1213800",
                "dbid" : 11527886,
                "hash" : 211527886
            },
            "qty" : -1.0,
            "price" : 15.4642016528696
        },
        {
            "date" : pd.Timestamp("2012-11-14T12:45:00"),
            "usdvalue" : 430.408010149009,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1214000",
                "dbid" : 11527888,
                "hash" : 211527888
            },
            "qty" : 1.0,
            "price" : 8.60816020298017
        },
        {
            "date" : pd.Timestamp("2012-12-19T12:45:00"),
            "usdvalue" : -72025.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ12",
                "dbid" : 3408,
                "hash" : 100003408
            },
            "qty" : -1.0,
            "price" : 1440.5
        },
        {
            "date" : pd.Timestamp("2012-12-19T12:45:00"),
            "usdvalue" : -2042.31859789111,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1214000",
                "dbid" : 11527888,
                "hash" : 211527888
            },
            "qty" : -1.0,
            "price" : 40.8463719578222
        },
        {
            "date" : pd.Timestamp("2012-12-19T12:45:00"),
            "usdvalue" : 3033.76341655612,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1213800",
                "dbid" : 11527886,
                "hash" : 211527886
            },
            "qty" : 1.0,
            "price" : 60.6752683311224
        },
        {
            "date" : pd.Timestamp("2012-12-19T12:45:00"),
            "usdvalue" : -1.710759871079,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1213300",
                "dbid" : 11528015,
                "hash" : 211528015
            },
            "qty" : -1.0,
            "price" : 0.0342151974215801
        },
        {
            "date" : pd.Timestamp("2012-12-19T12:45:00"),
            "usdvalue" : 708.177206493852,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1314100",
                "dbid" : 5945212,
                "hash" : 205945212
            },
            "qty" : 1.0,
            "price" : 14.163544129877
        },
        {
            "date" : pd.Timestamp("2012-12-19T12:45:00"),
            "usdvalue" : 71812.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH13",
                "dbid" : 3704,
                "hash" : 100003704
            },
            "qty" : 1.0,
            "price" : 1436.25
        },
        {
            "date" : pd.Timestamp("2012-12-19T12:45:00"),
            "usdvalue" : -596.319783038848,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1314600",
                "dbid" : 5944038,
                "hash" : 205944038
            },
            "qty" : -1.0,
            "price" : 11.926395660777
        },
        {
            "date" : pd.Timestamp("2012-12-19T12:45:00"),
            "usdvalue" : 297.761115972256,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1314800",
                "dbid" : 5944041,
                "hash" : 205944041
            },
            "qty" : 1.0,
            "price" : 5.95522231944511
        },
        {
            "date" : pd.Timestamp("2013-01-16T12:45:00"),
            "usdvalue" : -73375.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH13",
                "dbid" : 3704,
                "hash" : 100003704
            },
            "qty" : -1.0,
            "price" : 1467.5
        },
        {
            "date" : pd.Timestamp("2013-01-16T12:45:00"),
            "usdvalue" : -57.7720907964832,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1314800",
                "dbid" : 5944041,
                "hash" : 205944041
            },
            "qty" : -1.0,
            "price" : 1.15544181592966
        },
        {
            "date" : pd.Timestamp("2013-01-16T12:45:00"),
            "usdvalue" : -2.1391986442663,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1314100",
                "dbid" : 5945212,
                "hash" : 205945212
            },
            "qty" : -1.0,
            "price" : 0.0427839728853261
        },
        {
            "date" : pd.Timestamp("2013-01-16T12:45:00"),
            "usdvalue" : 504.171436375736,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1314600",
                "dbid" : 5944038,
                "hash" : 205944038
            },
            "qty" : 1.0,
            "price" : 10.0834287275147
        },
        {
            "date" : pd.Timestamp("2013-01-16T12:45:00"),
            "usdvalue" : 572.257028365811,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1314400",
                "dbid" : 5945993,
                "hash" : 205945993
            },
            "qty" : 1.0,
            "price" : 11.4451405673162
        },
        {
            "date" : pd.Timestamp("2013-01-16T12:45:00"),
            "usdvalue" : 73375.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH13",
                "dbid" : 3704,
                "hash" : 100003704
            },
            "qty" : 1.0,
            "price" : 1467.5
        },
        {
            "date" : pd.Timestamp("2013-01-16T12:45:00"),
            "usdvalue" : -477.526325379262,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1314900",
                "dbid" : 5944799,
                "hash" : 205944799
            },
            "qty" : -1.0,
            "price" : 9.55052650758523
        },
        {
            "date" : pd.Timestamp("2013-01-16T12:45:00"),
            "usdvalue" : 197.810949253251,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1315100",
                "dbid" : 5944944,
                "hash" : 205944944
            },
            "qty" : 1.0,
            "price" : 3.95621898506502
        },
        {
            "date" : pd.Timestamp("2013-02-13T12:45:00"),
            "usdvalue" : -75762.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH13",
                "dbid" : 3704,
                "hash" : 100003704
            },
            "qty" : -1.0,
            "price" : 1515.25
        },
        {
            "date" : pd.Timestamp("2013-02-13T12:45:00"),
            "usdvalue" : -2.89276965062104,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1314400",
                "dbid" : 5945993,
                "hash" : 205945993
            },
            "qty" : -1.0,
            "price" : 0.0578553930124208
        },
        {
            "date" : pd.Timestamp("2013-02-13T12:45:00"),
            "usdvalue" : -414.167105381438,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1315100",
                "dbid" : 5944944,
                "hash" : 205944944
            },
            "qty" : -1.0,
            "price" : 8.28334210762876
        },
        {
            "date" : pd.Timestamp("2013-02-13T12:45:00"),
            "usdvalue" : 1290.32295006139,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1314900",
                "dbid" : 5944799,
                "hash" : 205944799
            },
            "qty" : 1.0,
            "price" : 25.8064590012277
        },
        {
            "date" : pd.Timestamp("2013-02-13T12:45:00"),
            "usdvalue" : 544.147144551758,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1314900",
                "dbid" : 5946225,
                "hash" : 205946225
            },
            "qty" : 1.0,
            "price" : 10.8829428910352
        },
        {
            "date" : pd.Timestamp("2013-02-13T12:45:00"),
            "usdvalue" : 75762.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH13",
                "dbid" : 3704,
                "hash" : 100003704
            },
            "qty" : 1.0,
            "price" : 1515.25
        },
        {
            "date" : pd.Timestamp("2013-02-13T12:45:00"),
            "usdvalue" : -354.562107218993,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1315400",
                "dbid" : 5944690,
                "hash" : 205944690
            },
            "qty" : -1.0,
            "price" : 7.09124214437986
        },
        {
            "date" : pd.Timestamp("2013-02-13T12:45:00"),
            "usdvalue" : 119.411092941228,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1315600",
                "dbid" : 5944699,
                "hash" : 205944699
            },
            "qty" : 1.0,
            "price" : 2.38822185882455
        },
        {
            "date" : pd.Timestamp("2013-03-13T12:45:00"),
            "usdvalue" : -77712.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH13",
                "dbid" : 3704,
                "hash" : 100003704
            },
            "qty" : -1.0,
            "price" : 1554.25
        },
        {
            "date" : pd.Timestamp("2013-03-13T12:45:00"),
            "usdvalue" : -3.53968526007433,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1314900",
                "dbid" : 5946225,
                "hash" : 205946225
            },
            "qty" : -1.0,
            "price" : 0.0707937052014866
        },
        {
            "date" : pd.Timestamp("2013-03-13T12:45:00"),
            "usdvalue" : 767.37287416903,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1315400",
                "dbid" : 5944690,
                "hash" : 205944690
            },
            "qty" : 1.0,
            "price" : 15.3474574833806
        },
        {
            "date" : pd.Timestamp("2013-03-13T12:45:00"),
            "usdvalue" : -98.4209419256814,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1315600",
                "dbid" : 5944699,
                "hash" : 205944699
            },
            "qty" : -1.0,
            "price" : 1.96841883851363
        },
        {
            "date" : pd.Timestamp("2013-03-13T12:45:00"),
            "usdvalue" : 681.522736683814,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1315250",
                "dbid" : 5946060,
                "hash" : 205946060
            },
            "qty" : 1.0,
            "price" : 13.6304547336763
        },
        {
            "date" : pd.Timestamp("2013-03-13T12:45:00"),
            "usdvalue" : 77425.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM13",
                "dbid" : 3981,
                "hash" : 100003981
            },
            "qty" : 1.0,
            "price" : 1548.5
        },
        {
            "date" : pd.Timestamp("2013-03-13T12:45:00"),
            "usdvalue" : -438.826060940514,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1315750",
                "dbid" : 5944269,
                "hash" : 205944269
            },
            "qty" : -1.0,
            "price" : 8.77652121881027
        },
        {
            "date" : pd.Timestamp("2013-03-13T12:45:00"),
            "usdvalue" : 191.157491404913,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1315950",
                "dbid" : 6190602,
                "hash" : 206190602
            },
            "qty" : 1.0,
            "price" : 3.82314982809825
        },
        {
            "date" : pd.Timestamp("2013-04-17T12:45:00"),
            "usdvalue" : -0.0410389008316331,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1315950",
                "dbid" : 6190602,
                "hash" : 206190602
            },
            "qty" : -1.0,
            "price" : 0.000820778016632662
        },
        {
            "date" : pd.Timestamp("2013-04-17T12:45:00"),
            "usdvalue" : -129.689324433383,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1315250",
                "dbid" : 5946060,
                "hash" : 205946060
            },
            "qty" : -1.0,
            "price" : 2.59378648866766
        },
        {
            "date" : pd.Timestamp("2013-04-17T12:45:00"),
            "usdvalue" : -77337.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM13",
                "dbid" : 3981,
                "hash" : 100003981
            },
            "qty" : -1.0,
            "price" : 1546.75
        },
        {
            "date" : pd.Timestamp("2013-04-17T12:45:00"),
            "usdvalue" : 7.85394922326148,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1315750",
                "dbid" : 5944269,
                "hash" : 205944269
            },
            "qty" : 1.0,
            "price" : 0.15707898446523
        },
        {
            "date" : pd.Timestamp("2013-04-17T12:45:00"),
            "usdvalue" : 740.587149293469,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1315200",
                "dbid" : 6393164,
                "hash" : 206393164
            },
            "qty" : 1.0,
            "price" : 14.8117429858694
        },
        {
            "date" : pd.Timestamp("2013-04-17T12:45:00"),
            "usdvalue" : 77337.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM13",
                "dbid" : 3981,
                "hash" : 100003981
            },
            "qty" : 1.0,
            "price" : 1546.75
        },
        {
            "date" : pd.Timestamp("2013-04-17T12:45:00"),
            "usdvalue" : -587.086594383135,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1315700",
                "dbid" : 6393054,
                "hash" : 206393054
            },
            "qty" : -1.0,
            "price" : 11.7417318876627
        },
        {
            "date" : pd.Timestamp("2013-04-17T12:45:00"),
            "usdvalue" : 258.60795151309,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1315900",
                "dbid" : 6393020,
                "hash" : 206393020
            },
            "qty" : 1.0,
            "price" : 5.17215903026181
        },
        {
            "date" : pd.Timestamp("2013-05-15T12:45:00"),
            "usdvalue" : -3303.86872444797,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1315900",
                "dbid" : 6393020,
                "hash" : 206393020
            },
            "qty" : -1.0,
            "price" : 66.0773744889593
        },
        {
            "date" : pd.Timestamp("2013-05-15T12:45:00"),
            "usdvalue" : -0.585332516228421,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1315200",
                "dbid" : 6393164,
                "hash" : 206393164
            },
            "qty" : -1.0,
            "price" : 0.0117066503245684
        },
        {
            "date" : pd.Timestamp("2013-05-15T12:45:00"),
            "usdvalue" : -82800.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM13",
                "dbid" : 3981,
                "hash" : 100003981
            },
            "qty" : -1.0,
            "price" : 1656.0
        },
        {
            "date" : pd.Timestamp("2013-05-15T12:45:00"),
            "usdvalue" : 4302.43282641258,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1315700",
                "dbid" : 6393054,
                "hash" : 206393054
            },
            "qty" : 1.0,
            "price" : 86.0486565282515
        },
        {
            "date" : pd.Timestamp("2013-05-15T12:45:00"),
            "usdvalue" : 735.935428160491,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1316300",
                "dbid" : 5946071,
                "hash" : 205946071
            },
            "qty" : 1.0,
            "price" : 14.7187085632098
        },
        {
            "date" : pd.Timestamp("2013-05-15T12:45:00"),
            "usdvalue" : 82800.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM13",
                "dbid" : 3981,
                "hash" : 100003981
            },
            "qty" : 1.0,
            "price" : 1656.0
        },
        {
            "date" : pd.Timestamp("2013-05-15T12:45:00"),
            "usdvalue" : -629.204828047665,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1316800",
                "dbid" : 5944474,
                "hash" : 205944474
            },
            "qty" : -1.0,
            "price" : 12.5840965609533
        },
        {
            "date" : pd.Timestamp("2013-05-15T12:45:00"),
            "usdvalue" : 351.149047654272,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1317000",
                "dbid" : 5944332,
                "hash" : 205944332
            },
            "qty" : 1.0,
            "price" : 7.02298095308544
        },
        {
            "date" : pd.Timestamp("2013-06-19T12:45:00"),
            "usdvalue" : 1.44336589226945,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1316800",
                "dbid" : 5944474,
                "hash" : 205944474
            },
            "qty" : 1.0,
            "price" : 0.0288673178453891
        },
        {
            "date" : pd.Timestamp("2013-06-19T12:45:00"),
            "usdvalue" : -0.0559665167952694,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1317000",
                "dbid" : 5944332,
                "hash" : 205944332
            },
            "qty" : -1.0,
            "price" : 0.00111933033590539
        },
        {
            "date" : pd.Timestamp("2013-06-19T12:45:00"),
            "usdvalue" : -81687.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM13",
                "dbid" : 3981,
                "hash" : 100003981
            },
            "qty" : -1.0,
            "price" : 1633.75
        },
        {
            "date" : pd.Timestamp("2013-06-19T12:45:00"),
            "usdvalue" : -392.138805812289,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1316300",
                "dbid" : 5946071,
                "hash" : 205946071
            },
            "qty" : -1.0,
            "price" : 7.84277611624577
        },
        {
            "date" : pd.Timestamp("2013-06-19T12:45:00"),
            "usdvalue" : 1059.47270106648,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1316100",
                "dbid" : 7641259,
                "hash" : 207641259
            },
            "qty" : 1.0,
            "price" : 21.1894540213295
        },
        {
            "date" : pd.Timestamp("2013-06-19T12:45:00"),
            "usdvalue" : 81700.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU13",
                "dbid" : 4546,
                "hash" : 100004546
            },
            "qty" : 1.0,
            "price" : 1634.0
        },
        {
            "date" : pd.Timestamp("2013-06-19T12:45:00"),
            "usdvalue" : -794.127072445167,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1316600",
                "dbid" : 7641107,
                "hash" : 207641107
            },
            "qty" : -1.0,
            "price" : 15.8825414489033
        },
        {
            "date" : pd.Timestamp("2013-06-19T12:45:00"),
            "usdvalue" : 417.96728365139,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1316800",
                "dbid" : 7641109,
                "hash" : 207641109
            },
            "qty" : 1.0,
            "price" : 8.3593456730278
        },
        {
            "date" : pd.Timestamp("2013-07-17T12:45:00"),
            "usdvalue" : -81700.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU13",
                "dbid" : 4546,
                "hash" : 100004546
            },
            "qty" : -1.0,
            "price" : 1634.0
        },
        {
            "date" : pd.Timestamp("2013-07-17T12:45:00"),
            "usdvalue" : 31.2791040449163,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1316600",
                "dbid" : 7641107,
                "hash" : 207641107
            },
            "qty" : 1.0,
            "price" : 0.625582080898326
        },
        {
            "date" : pd.Timestamp("2013-07-17T12:45:00"),
            "usdvalue" : -124.264493377294,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1316100",
                "dbid" : 7641259,
                "hash" : 207641259
            },
            "qty" : -1.0,
            "price" : 2.48528986754587
        },
        {
            "date" : pd.Timestamp("2013-07-17T12:45:00"),
            "usdvalue" : -1.15651172445701,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1316800",
                "dbid" : 7641109,
                "hash" : 207641109
            },
            "qty" : -1.0,
            "price" : 0.0231302344891402
        },
        {
            "date" : pd.Timestamp("2013-07-17T12:45:00"),
            "usdvalue" : 920.861169046344,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1316100",
                "dbid" : 9056483,
                "hash" : 209056483
            },
            "qty" : 1.0,
            "price" : 18.4172233809269
        },
        {
            "date" : pd.Timestamp("2013-07-17T12:45:00"),
            "usdvalue" : 81700.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU13",
                "dbid" : 4546,
                "hash" : 100004546
            },
            "qty" : 1.0,
            "price" : 1634.0
        },
        {
            "date" : pd.Timestamp("2013-07-17T12:45:00"),
            "usdvalue" : -725.469082899997,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1316600",
                "dbid" : 9056294,
                "hash" : 209056294
            },
            "qty" : -1.0,
            "price" : 14.5093816579999
        },
        {
            "date" : pd.Timestamp("2013-07-17T12:45:00"),
            "usdvalue" : 407.445701132522,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1316800",
                "dbid" : 9056296,
                "hash" : 209056296
            },
            "qty" : 1.0,
            "price" : 8.14891402265044
        },
        {
            "date" : pd.Timestamp("2013-08-14T12:45:00"),
            "usdvalue" : -402.969437082993,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1316800",
                "dbid" : 9056296,
                "hash" : 209056296
            },
            "qty" : -1.0,
            "price" : 8.05938874165986
        },
        {
            "date" : pd.Timestamp("2013-08-14T12:45:00"),
            "usdvalue" : -84187.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU13",
                "dbid" : 4546,
                "hash" : 100004546
            },
            "qty" : -1.0,
            "price" : 1683.75
        },
        {
            "date" : pd.Timestamp("2013-08-14T12:45:00"),
            "usdvalue" : -5.03963351339483,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1316100",
                "dbid" : 9056483,
                "hash" : 209056483
            },
            "qty" : -1.0,
            "price" : 0.100792670267897
        },
        {
            "date" : pd.Timestamp("2013-08-14T12:45:00"),
            "usdvalue" : 1229.97908767471,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1316600",
                "dbid" : 9056294,
                "hash" : 209056294
            },
            "qty" : 1.0,
            "price" : 24.5995817534942
        },
        {
            "date" : pd.Timestamp("2013-08-14T12:45:00"),
            "usdvalue" : 877.586752428982,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1316600",
                "dbid" : 5945563,
                "hash" : 205945563
            },
            "qty" : 1.0,
            "price" : 17.5517350485796
        },
        {
            "date" : pd.Timestamp("2013-08-14T12:45:00"),
            "usdvalue" : 84187.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU13",
                "dbid" : 4546,
                "hash" : 100004546
            },
            "qty" : 1.0,
            "price" : 1683.75
        },
        {
            "date" : pd.Timestamp("2013-08-14T12:45:00"),
            "usdvalue" : -628.757133734882,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1317100",
                "dbid" : 5944393,
                "hash" : 205944393
            },
            "qty" : -1.0,
            "price" : 12.5751426746976
        },
        {
            "date" : pd.Timestamp("2013-08-14T12:45:00"),
            "usdvalue" : 304.463738662702,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1317300",
                "dbid" : 5944396,
                "hash" : 205944396
            },
            "qty" : 1.0,
            "price" : 6.08927477325403
        },
        {
            "date" : pd.Timestamp("2013-09-18T12:45:00"),
            "usdvalue" : 882.32997096502,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1317100",
                "dbid" : 5944393,
                "hash" : 205944393
            },
            "qty" : 1.0,
            "price" : 17.6465994193004
        },
        {
            "date" : pd.Timestamp("2013-09-18T12:45:00"),
            "usdvalue" : -86275.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU13",
                "dbid" : 4546,
                "hash" : 100004546
            },
            "qty" : -1.0,
            "price" : 1725.5
        },
        {
            "date" : pd.Timestamp("2013-09-18T12:45:00"),
            "usdvalue" : -1.78137357959787,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1316600",
                "dbid" : 5945563,
                "hash" : 205945563
            },
            "qty" : -1.0,
            "price" : 0.0356274715919573
        },
        {
            "date" : pd.Timestamp("2013-09-18T12:45:00"),
            "usdvalue" : -258.88653247323,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1317300",
                "dbid" : 5944396,
                "hash" : 205944396
            },
            "qty" : -1.0,
            "price" : 5.17773064946459
        },
        {
            "date" : pd.Timestamp("2013-09-18T12:45:00"),
            "usdvalue" : 772.819424890582,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1316950",
                "dbid" : 10303620,
                "hash" : 210303620
            },
            "qty" : 1.0,
            "price" : 15.4563884978116
        },
        {
            "date" : pd.Timestamp("2013-09-18T12:45:00"),
            "usdvalue" : 85937.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ13",
                "dbid" : 4578,
                "hash" : 100004578
            },
            "qty" : 1.0,
            "price" : 1718.75
        },
        {
            "date" : pd.Timestamp("2013-09-18T12:45:00"),
            "usdvalue" : -550.754671359471,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1317450",
                "dbid" : 10418236,
                "hash" : 210418236
            },
            "qty" : -1.0,
            "price" : 11.0150934271894
        },
        {
            "date" : pd.Timestamp("2013-09-18T12:45:00"),
            "usdvalue" : 270.366680166748,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1317650",
                "dbid" : 10612494,
                "hash" : 210612494
            },
            "qty" : 1.0,
            "price" : 5.40733360333496
        },
        {
            "date" : pd.Timestamp("2013-10-16T12:45:00"),
            "usdvalue" : 50.7490135372365,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1317450",
                "dbid" : 10418236,
                "hash" : 210418236
            },
            "qty" : 1.0,
            "price" : 1.01498027074473
        },
        {
            "date" : pd.Timestamp("2013-10-16T12:45:00"),
            "usdvalue" : -85700.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ13",
                "dbid" : 4578,
                "hash" : 100004578
            },
            "qty" : -1.0,
            "price" : 1714.0
        },
        {
            "date" : pd.Timestamp("2013-10-16T12:45:00"),
            "usdvalue" : -239.492833222863,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1316950",
                "dbid" : 10303620,
                "hash" : 210303620
            },
            "qty" : -1.0,
            "price" : 4.78985666445726
        },
        {
            "date" : pd.Timestamp("2013-10-16T12:45:00"),
            "usdvalue" : -15.2867984271094,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1317650",
                "dbid" : 10612494,
                "hash" : 210612494
            },
            "qty" : -1.0,
            "price" : 0.305735968542187
        },
        {
            "date" : pd.Timestamp("2013-10-16T12:45:00"),
            "usdvalue" : 1024.40396776639,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1316900",
                "dbid" : 10890920,
                "hash" : 210890920
            },
            "qty" : 1.0,
            "price" : 20.4880793553277
        },
        {
            "date" : pd.Timestamp("2013-10-16T12:45:00"),
            "usdvalue" : 85700.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ13",
                "dbid" : 4578,
                "hash" : 100004578
            },
            "qty" : 1.0,
            "price" : 1714.0
        },
        {
            "date" : pd.Timestamp("2013-10-16T12:45:00"),
            "usdvalue" : -762.32663013086,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1317400",
                "dbid" : 10890631,
                "hash" : 210890631
            },
            "qty" : -1.0,
            "price" : 15.2465326026172
        },
        {
            "date" : pd.Timestamp("2013-10-16T12:45:00"),
            "usdvalue" : 415.236624552551,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1317600",
                "dbid" : 10890635,
                "hash" : 210890635
            },
            "qty" : 1.0,
            "price" : 8.30473249105103
        },
        {
            "date" : pd.Timestamp("2013-11-13T12:45:00"),
            "usdvalue" : -2.46221095048647,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1316900",
                "dbid" : 10890920,
                "hash" : 210890920
            },
            "qty" : -1.0,
            "price" : 0.0492442190097293
        },
        {
            "date" : pd.Timestamp("2013-11-13T12:45:00"),
            "usdvalue" : -88800.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ13",
                "dbid" : 4578,
                "hash" : 100004578
            },
            "qty" : -1.0,
            "price" : 1776.0
        },
        {
            "date" : pd.Timestamp("2013-11-13T12:45:00"),
            "usdvalue" : -874.71614815895,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1317600",
                "dbid" : 10890635,
                "hash" : 210890635
            },
            "qty" : -1.0,
            "price" : 17.494322963179
        },
        {
            "date" : pd.Timestamp("2013-11-13T12:45:00"),
            "usdvalue" : 1816.04451740446,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1317400",
                "dbid" : 10890631,
                "hash" : 210890631
            },
            "qty" : 1.0,
            "price" : 36.3208903480893
        },
        {
            "date" : pd.Timestamp("2013-11-13T12:45:00"),
            "usdvalue" : 795.266021166293,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1317500",
                "dbid" : 5946231,
                "hash" : 205946231
            },
            "qty" : 1.0,
            "price" : 15.9053204233259
        },
        {
            "date" : pd.Timestamp("2013-11-13T12:45:00"),
            "usdvalue" : 88800.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ13",
                "dbid" : 4578,
                "hash" : 100004578
            },
            "qty" : 1.0,
            "price" : 1776.0
        },
        {
            "date" : pd.Timestamp("2013-11-13T12:45:00"),
            "usdvalue" : -646.883048786987,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1318000",
                "dbid" : 5945153,
                "hash" : 205945153
            },
            "qty" : -1.0,
            "price" : 12.9376609757397
        },
        {
            "date" : pd.Timestamp("2013-11-13T12:45:00"),
            "usdvalue" : 334.752045597455,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1318200",
                "dbid" : 8197015,
                "hash" : 208197015
            },
            "qty" : 1.0,
            "price" : 6.69504091194909
        },
        {
            "date" : pd.Timestamp("2013-12-18T12:45:00"),
            "usdvalue" : 758.272514166242,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1318000",
                "dbid" : 5945153,
                "hash" : 205945153
            },
            "qty" : 1.0,
            "price" : 15.1654502833248
        },
        {
            "date" : pd.Timestamp("2013-12-18T12:45:00"),
            "usdvalue" : -90500.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ13",
                "dbid" : 4578,
                "hash" : 100004578
            },
            "qty" : -1.0,
            "price" : 1810.0
        },
        {
            "date" : pd.Timestamp("2013-12-18T12:45:00"),
            "usdvalue" : -8.00306638402049,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1317500",
                "dbid" : 5946231,
                "hash" : 205946231
            },
            "qty" : -1.0,
            "price" : 0.16006132768041
        },
        {
            "date" : pd.Timestamp("2013-12-18T12:45:00"),
            "usdvalue" : -240.437830952345,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1318200",
                "dbid" : 8197015,
                "hash" : 208197015
            },
            "qty" : -1.0,
            "price" : 4.8087566190469
        },
        {
            "date" : pd.Timestamp("2013-12-18T12:45:00"),
            "usdvalue" : 867.203925051194,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1417800",
                "dbid" : 11489002,
                "hash" : 211489002
            },
            "qty" : 1.0,
            "price" : 17.3440785010239
        },
        {
            "date" : pd.Timestamp("2013-12-18T12:45:00"),
            "usdvalue" : 90187.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH14",
                "dbid" : 4736,
                "hash" : 100004736
            },
            "qty" : 1.0,
            "price" : 1803.75
        },
        {
            "date" : pd.Timestamp("2013-12-18T12:45:00"),
            "usdvalue" : -646.969191874848,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1418300",
                "dbid" : 11488846,
                "hash" : 211488846
            },
            "qty" : -1.0,
            "price" : 12.939383837497
        },
        {
            "date" : pd.Timestamp("2013-12-18T12:45:00"),
            "usdvalue" : 341.089561791421,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1418500",
                "dbid" : 11488848,
                "hash" : 211488848
            },
            "qty" : 1.0,
            "price" : 6.82179123582841
        },
        {
            "date" : pd.Timestamp("2014-01-15T12:45:00"),
            "usdvalue" : -92162.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH14",
                "dbid" : 4736,
                "hash" : 100004736
            },
            "qty" : -1.0,
            "price" : 1843.25
        },
        {
            "date" : pd.Timestamp("2014-01-15T12:45:00"),
            "usdvalue" : -144.041592112529,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1418500",
                "dbid" : 11488848,
                "hash" : 211488848
            },
            "qty" : -1.0,
            "price" : 2.88083184225059
        },
        {
            "date" : pd.Timestamp("2014-01-15T12:45:00"),
            "usdvalue" : -1.18391608604811,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1417800",
                "dbid" : 11489002,
                "hash" : 211489002
            },
            "qty" : -1.0,
            "price" : 0.0236783217209622
        },
        {
            "date" : pd.Timestamp("2014-01-15T12:45:00"),
            "usdvalue" : 750.541757564031,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1418300",
                "dbid" : 11488846,
                "hash" : 211488846
            },
            "qty" : 1.0,
            "price" : 15.0108351512806
        },
        {
            "date" : pd.Timestamp("2014-01-15T12:45:00"),
            "usdvalue" : 838.388117123452,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1418200",
                "dbid" : 11536040,
                "hash" : 211536040
            },
            "qty" : 1.0,
            "price" : 16.767762342469
        },
        {
            "date" : pd.Timestamp("2014-01-15T12:45:00"),
            "usdvalue" : 92162.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH14",
                "dbid" : 4736,
                "hash" : 100004736
            },
            "qty" : 1.0,
            "price" : 1843.25
        },
        {
            "date" : pd.Timestamp("2014-01-15T12:45:00"),
            "usdvalue" : -578.867498197701,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1418700",
                "dbid" : 11535286,
                "hash" : 211535286
            },
            "qty" : -1.0,
            "price" : 11.577349963954
        },
        {
            "date" : pd.Timestamp("2014-01-15T12:45:00"),
            "usdvalue" : 282.726177715966,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1418900",
                "dbid" : 11535290,
                "hash" : 211535290
            },
            "qty" : 1.0,
            "price" : 5.65452355431933
        },
        {
            "date" : pd.Timestamp("2014-02-19T12:45:00"),
            "usdvalue" : -229.680231737842,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1418200",
                "dbid" : 11536040,
                "hash" : 211536040
            },
            "qty" : -1.0,
            "price" : 4.59360463475684
        },
        {
            "date" : pd.Timestamp("2014-02-19T12:45:00"),
            "usdvalue" : -91287.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH14",
                "dbid" : 4736,
                "hash" : 100004736
            },
            "qty" : -1.0,
            "price" : 1825.75
        },
        {
            "date" : pd.Timestamp("2014-02-19T12:45:00"),
            "usdvalue" : -0.20313562663925,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1418900",
                "dbid" : 11535290,
                "hash" : 211535290
            },
            "qty" : -1.0,
            "price" : 0.00406271253278501
        },
        {
            "date" : pd.Timestamp("2014-02-19T12:45:00"),
            "usdvalue" : 0.705077559260125,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1418700",
                "dbid" : 11535286,
                "hash" : 211535286
            },
            "qty" : 1.0,
            "price" : 0.0141015511852025
        },
        {
            "date" : pd.Timestamp("2014-02-19T12:45:00"),
            "usdvalue" : 840.200174155495,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1418000",
                "dbid" : 8341223,
                "hash" : 208341223
            },
            "qty" : 1.0,
            "price" : 16.8040034831099
        },
        {
            "date" : pd.Timestamp("2014-02-19T12:45:00"),
            "usdvalue" : 91287.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH14",
                "dbid" : 4736,
                "hash" : 100004736
            },
            "qty" : 1.0,
            "price" : 1825.75
        },
        {
            "date" : pd.Timestamp("2014-02-19T12:45:00"),
            "usdvalue" : -666.422354318377,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1418500",
                "dbid" : 8341049,
                "hash" : 208341049
            },
            "qty" : -1.0,
            "price" : 13.3284470863675
        },
        {
            "date" : pd.Timestamp("2014-02-19T12:45:00"),
            "usdvalue" : 337.774497046021,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1418700",
                "dbid" : 8855413,
                "hash" : 208855413
            },
            "qty" : 1.0,
            "price" : 6.75548994092043
        },
        {
            "date" : pd.Timestamp("2014-03-19T12:45:00"),
            "usdvalue" : -93162.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH14",
                "dbid" : 4736,
                "hash" : 100004736
            },
            "qty" : -1.0,
            "price" : 1863.25
        },
        {
            "date" : pd.Timestamp("2014-03-19T12:45:00"),
            "usdvalue" : 818.333577910948,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1418500",
                "dbid" : 8341049,
                "hash" : 208341049
            },
            "qty" : 1.0,
            "price" : 16.366671558219
        },
        {
            "date" : pd.Timestamp("2014-03-19T12:45:00"),
            "usdvalue" : -202.918333137012,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1418700",
                "dbid" : 8855413,
                "hash" : 208855413
            },
            "qty" : -1.0,
            "price" : 4.05836666274024
        },
        {
            "date" : pd.Timestamp("2014-03-19T12:45:00"),
            "usdvalue" : -9.97945925001424,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1418000",
                "dbid" : 8341223,
                "hash" : 208341223
            },
            "qty" : -1.0,
            "price" : 0.199589185000285
        },
        {
            "date" : pd.Timestamp("2014-03-19T12:45:00"),
            "usdvalue" : 927.492551151028,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1418300",
                "dbid" : 11536293,
                "hash" : 211536293
            },
            "qty" : 1.0,
            "price" : 18.5498510230206
        },
        {
            "date" : pd.Timestamp("2014-03-19T12:45:00"),
            "usdvalue" : 92787.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM14",
                "dbid" : 4738,
                "hash" : 100004738
            },
            "qty" : 1.0,
            "price" : 1855.75
        },
        {
            "date" : pd.Timestamp("2014-03-19T12:45:00"),
            "usdvalue" : -721.492940648625,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1418800",
                "dbid" : 11535539,
                "hash" : 211535539
            },
            "qty" : -1.0,
            "price" : 14.4298588129725
        },
        {
            "date" : pd.Timestamp("2014-03-19T12:45:00"),
            "usdvalue" : 355.04656738411,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1419000",
                "dbid" : 11535543,
                "hash" : 211535543
            },
            "qty" : 1.0,
            "price" : 7.10093134768221
        },
        {
            "date" : pd.Timestamp("2014-04-15T12:45:00"),
            "usdvalue" : -91725.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM14",
                "dbid" : 4738,
                "hash" : 100004738
            },
            "qty" : -1.0,
            "price" : 1834.5
        },
        {
            "date" : pd.Timestamp("2014-04-15T12:45:00"),
            "usdvalue" : 10.1997025073253,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1418800",
                "dbid" : 11535539,
                "hash" : 211535539
            },
            "qty" : 1.0,
            "price" : 0.203994050146505
        },
        {
            "date" : pd.Timestamp("2014-04-15T12:45:00"),
            "usdvalue" : -352.42046068999,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1418300",
                "dbid" : 11536293,
                "hash" : 211536293
            },
            "qty" : -1.0,
            "price" : 7.0484092137998
        },
        {
            "date" : pd.Timestamp("2014-04-15T12:45:00"),
            "usdvalue" : -2.68450103445179,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1419000",
                "dbid" : 11535543,
                "hash" : 211535543
            },
            "qty" : -1.0,
            "price" : 0.0536900206890358
        },
        {
            "date" : pd.Timestamp("2014-04-15T12:45:00"),
            "usdvalue" : 1058.17690971959,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1418100",
                "dbid" : 11549139,
                "hash" : 211549139
            },
            "qty" : 1.0,
            "price" : 21.1635381943918
        },
        {
            "date" : pd.Timestamp("2014-04-15T12:45:00"),
            "usdvalue" : 91725.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM14",
                "dbid" : 4738,
                "hash" : 100004738
            },
            "qty" : 1.0,
            "price" : 1834.5
        },
        {
            "date" : pd.Timestamp("2014-04-15T12:45:00"),
            "usdvalue" : -818.570119747466,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1418600",
                "dbid" : 11548933,
                "hash" : 211548933
            },
            "qty" : -1.0,
            "price" : 16.3714023949493
        },
        {
            "date" : pd.Timestamp("2014-04-15T12:45:00"),
            "usdvalue" : 445.923114449383,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1418800",
                "dbid" : 11548937,
                "hash" : 211548937
            },
            "qty" : 1.0,
            "price" : 8.91846228898766
        },
        {
            "date" : pd.Timestamp("2014-05-14T12:45:00"),
            "usdvalue" : -431.939628466137,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1418800",
                "dbid" : 11548937,
                "hash" : 211548937
            },
            "qty" : -1.0,
            "price" : 8.63879256932273
        },
        {
            "date" : pd.Timestamp("2014-05-14T12:45:00"),
            "usdvalue" : -94212.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM14",
                "dbid" : 4738,
                "hash" : 100004738
            },
            "qty" : -1.0,
            "price" : 1884.25
        },
        {
            "date" : pd.Timestamp("2014-05-14T12:45:00"),
            "usdvalue" : -3.52674517352147,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1418100",
                "dbid" : 11549139,
                "hash" : 211549139
            },
            "qty" : -1.0,
            "price" : 0.0705349034704295
        },
        {
            "date" : pd.Timestamp("2014-05-14T12:45:00"),
            "usdvalue" : 1255.70464368502,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1418600",
                "dbid" : 11548933,
                "hash" : 211548933
            },
            "qty" : 1.0,
            "price" : 25.1140928737004
        },
        {
            "date" : pd.Timestamp("2014-05-14T12:45:00"),
            "usdvalue" : 941.806483948568,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1418600",
                "dbid" : 10333759,
                "hash" : 210333759
            },
            "qty" : 1.0,
            "price" : 18.8361296789714
        },
        {
            "date" : pd.Timestamp("2014-05-14T12:45:00"),
            "usdvalue" : 94212.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM14",
                "dbid" : 4738,
                "hash" : 100004738
            },
            "qty" : 1.0,
            "price" : 1884.25
        },
        {
            "date" : pd.Timestamp("2014-05-14T12:45:00"),
            "usdvalue" : -703.672741716451,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1419100",
                "dbid" : 10333642,
                "hash" : 210333642
            },
            "qty" : -1.0,
            "price" : 14.073454834329
        },
        {
            "date" : pd.Timestamp("2014-05-14T12:45:00"),
            "usdvalue" : 365.922765020557,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1419300",
                "dbid" : 10333647,
                "hash" : 210333647
            },
            "qty" : 1.0,
            "price" : 7.31845530041113
        },
        {
            "date" : pd.Timestamp("2014-06-18T12:45:00"),
            "usdvalue" : -97837.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM14",
                "dbid" : 4738,
                "hash" : 100004738
            },
            "qty" : -1.0,
            "price" : 1956.75
        },
        {
            "date" : pd.Timestamp("2014-06-18T12:45:00"),
            "usdvalue" : -1364.64578777395,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1419300",
                "dbid" : 10333647,
                "hash" : 210333647
            },
            "qty" : -1.0,
            "price" : 27.292915755479
        },
        {
            "date" : pd.Timestamp("2014-06-18T12:45:00"),
            "usdvalue" : 2344.47930911118,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1419100",
                "dbid" : 10333642,
                "hash" : 210333642
            },
            "qty" : 1.0,
            "price" : 46.8895861822236
        },
        {
            "date" : pd.Timestamp("2014-06-18T12:45:00"),
            "usdvalue" : -1.45944061377223,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1418600",
                "dbid" : 10333759,
                "hash" : 210333759
            },
            "qty" : -1.0,
            "price" : 0.0291888122754447
        },
        {
            "date" : pd.Timestamp("2014-06-18T12:45:00"),
            "usdvalue" : 674.858724288299,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1419250",
                "dbid" : 11555789,
                "hash" : 211555789
            },
            "qty" : 1.0,
            "price" : 13.497174485766
        },
        {
            "date" : pd.Timestamp("2014-06-18T12:45:00"),
            "usdvalue" : 97450.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU14",
                "dbid" : 4745,
                "hash" : 100004745
            },
            "qty" : 1.0,
            "price" : 1949.0
        },
        {
            "date" : pd.Timestamp("2014-06-18T12:45:00"),
            "usdvalue" : -447.474860251901,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1419750",
                "dbid" : 11555615,
                "hash" : 211555615
            },
            "qty" : -1.0,
            "price" : 8.94949720503803
        },
        {
            "date" : pd.Timestamp("2014-06-18T12:45:00"),
            "usdvalue" : 191.403495750177,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1419950",
                "dbid" : 11562002,
                "hash" : 211562002
            },
            "qty" : 1.0,
            "price" : 3.82806991500354
        },
        {
            "date" : pd.Timestamp("2014-07-16T12:45:00"),
            "usdvalue" : -98750.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU14",
                "dbid" : 4745,
                "hash" : 100004745
            },
            "qty" : -1.0,
            "price" : 1975.0
        },
        {
            "date" : pd.Timestamp("2014-07-16T12:45:00"),
            "usdvalue" : -15.2067570505956,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1419950",
                "dbid" : 11562002,
                "hash" : 211562002
            },
            "qty" : -1.0,
            "price" : 0.304135141011912
        },
        {
            "date" : pd.Timestamp("2014-07-16T12:45:00"),
            "usdvalue" : -8.43630844825292,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1419250",
                "dbid" : 11555789,
                "hash" : 211555789
            },
            "qty" : -1.0,
            "price" : 0.168726168965058
        },
        {
            "date" : pd.Timestamp("2014-07-16T12:45:00"),
            "usdvalue" : 266.388122970596,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1419750",
                "dbid" : 11555615,
                "hash" : 211555615
            },
            "qty" : 1.0,
            "price" : 5.32776245941193
        },
        {
            "date" : pd.Timestamp("2014-07-16T12:45:00"),
            "usdvalue" : 696.606083307557,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1419500",
                "dbid" : 11566465,
                "hash" : 211566465
            },
            "qty" : 1.0,
            "price" : 13.9321216661511
        },
        {
            "date" : pd.Timestamp("2014-07-16T12:45:00"),
            "usdvalue" : 98750.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU14",
                "dbid" : 4745,
                "hash" : 100004745
            },
            "qty" : 1.0,
            "price" : 1975.0
        },
        {
            "date" : pd.Timestamp("2014-07-16T12:45:00"),
            "usdvalue" : -439.500234829319,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1420000",
                "dbid" : 11566250,
                "hash" : 211566250
            },
            "qty" : -1.0,
            "price" : 8.79000469658638
        },
        {
            "date" : pd.Timestamp("2014-07-16T12:45:00"),
            "usdvalue" : 161.681106223676,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1420200",
                "dbid" : 11566254,
                "hash" : 211566254
            },
            "qty" : 1.0,
            "price" : 3.23362212447353
        },
        {
            "date" : pd.Timestamp("2014-08-13T12:45:00"),
            "usdvalue" : -548.142422874082,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1419500",
                "dbid" : 11566465,
                "hash" : 211566465
            },
            "qty" : -1.0,
            "price" : 10.9628484574816
        },
        {
            "date" : pd.Timestamp("2014-08-13T12:45:00"),
            "usdvalue" : 2.12701911434623,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1420000",
                "dbid" : 11566250,
                "hash" : 211566250
            },
            "qty" : 1.0,
            "price" : 0.0425403822869246
        },
        {
            "date" : pd.Timestamp("2014-08-13T12:45:00"),
            "usdvalue" : -1.45036244248531,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1420200",
                "dbid" : 11566254,
                "hash" : 211566254
            },
            "qty" : -1.0,
            "price" : 0.0290072488497062
        },
        {
            "date" : pd.Timestamp("2014-08-13T12:45:00"),
            "usdvalue" : -97150.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU14",
                "dbid" : 4745,
                "hash" : 100004745
            },
            "qty" : -1.0,
            "price" : 1943.0
        },
        {
            "date" : pd.Timestamp("2014-08-13T12:45:00"),
            "usdvalue" : 1111.24475591616,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1419200",
                "dbid" : 11502723,
                "hash" : 211502723
            },
            "qty" : 1.0,
            "price" : 22.2248951183232
        },
        {
            "date" : pd.Timestamp("2014-08-13T12:45:00"),
            "usdvalue" : 97150.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU14",
                "dbid" : 4745,
                "hash" : 100004745
            },
            "qty" : 1.0,
            "price" : 1943.0
        },
        {
            "date" : pd.Timestamp("2014-08-13T12:45:00"),
            "usdvalue" : -780.442514242264,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1419700",
                "dbid" : 11502537,
                "hash" : 211502537
            },
            "qty" : -1.0,
            "price" : 15.6088502848453
        },
        {
            "date" : pd.Timestamp("2014-08-13T12:45:00"),
            "usdvalue" : 406.366976311804,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1419900",
                "dbid" : 11502540,
                "hash" : 211502540
            },
            "qty" : 1.0,
            "price" : 8.12733952623609
        },
        {
            "date" : pd.Timestamp("2014-09-17T12:45:00"),
            "usdvalue" : -100062.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU14",
                "dbid" : 4745,
                "hash" : 100004745
            },
            "qty" : -1.0,
            "price" : 2001.25
        },
        {
            "date" : pd.Timestamp("2014-09-17T12:45:00"),
            "usdvalue" : -6.36778267306291,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1419200",
                "dbid" : 11502723,
                "hash" : 211502723
            },
            "qty" : -1.0,
            "price" : 0.127355653461258
        },
        {
            "date" : pd.Timestamp("2014-09-17T12:45:00"),
            "usdvalue" : -741.377782101858,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1419900",
                "dbid" : 11502540,
                "hash" : 211502540
            },
            "qty" : -1.0,
            "price" : 14.8275556420372
        },
        {
            "date" : pd.Timestamp("2014-09-17T12:45:00"),
            "usdvalue" : 1613.85104439457,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1419700",
                "dbid" : 11502537,
                "hash" : 211502537
            },
            "qty" : 1.0,
            "price" : 32.2770208878915
        },
        {
            "date" : pd.Timestamp("2014-09-17T12:45:00"),
            "usdvalue" : 832.775642850993,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1419700",
                "dbid" : 11572210,
                "hash" : 211572210
            },
            "qty" : 1.0,
            "price" : 16.6555128570199
        },
        {
            "date" : pd.Timestamp("2014-09-17T12:45:00"),
            "usdvalue" : 99662.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ14",
                "dbid" : 4777,
                "hash" : 100004777
            },
            "qty" : 1.0,
            "price" : 1993.25
        },
        {
            "date" : pd.Timestamp("2014-09-17T12:45:00"),
            "usdvalue" : -501.650201978828,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1420200",
                "dbid" : 11572032,
                "hash" : 211572032
            },
            "qty" : -1.0,
            "price" : 10.0330040395766
        },
        {
            "date" : pd.Timestamp("2014-09-17T12:45:00"),
            "usdvalue" : 207.298733718849,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1420400",
                "dbid" : 11572035,
                "hash" : 211572035
            },
            "qty" : 1.0,
            "price" : 4.14597467437699
        },
        {
            "date" : pd.Timestamp("2014-10-15T12:45:00"),
            "usdvalue" : 0.0535496075569727,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1420200",
                "dbid" : 11572032,
                "hash" : 211572032
            },
            "qty" : 1.0,
            "price" : 0.00107099215113945
        },
        {
            "date" : pd.Timestamp("2014-10-15T12:45:00"),
            "usdvalue" : -92987.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ14",
                "dbid" : 4777,
                "hash" : 100004777
            },
            "qty" : -1.0,
            "price" : 1859.75
        },
        {
            "date" : pd.Timestamp("2014-10-15T12:45:00"),
            "usdvalue" : -5511.74140190292,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1419700",
                "dbid" : 11572210,
                "hash" : 211572210
            },
            "qty" : -1.0,
            "price" : 110.234828038058
        },
        {
            "date" : pd.Timestamp("2014-10-15T12:45:00"),
            "usdvalue" : -0.0593084415774353,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1420400",
                "dbid" : 11572035,
                "hash" : 211572035
            },
            "qty" : -1.0,
            "price" : 0.00118616883154871
        },
        {
            "date" : pd.Timestamp("2014-10-15T12:45:00"),
            "usdvalue" : 1876.94994601358,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1418350",
                "dbid" : 11604477,
                "hash" : 211604477
            },
            "qty" : 1.0,
            "price" : 37.5389989202716
        },
        {
            "date" : pd.Timestamp("2014-10-15T12:45:00"),
            "usdvalue" : 92987.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ14",
                "dbid" : 4777,
                "hash" : 100004777
            },
            "qty" : 1.0,
            "price" : 1859.75
        },
        {
            "date" : pd.Timestamp("2014-10-15T12:45:00"),
            "usdvalue" : -1612.75018890632,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1418850",
                "dbid" : 11604255,
                "hash" : 211604255
            },
            "qty" : -1.0,
            "price" : 32.2550037781264
        },
        {
            "date" : pd.Timestamp("2014-10-15T12:45:00"),
            "usdvalue" : 1139.21284536904,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1419050",
                "dbid" : 11604259,
                "hash" : 211604259
            },
            "qty" : 1.0,
            "price" : 22.7842569073807
        },
        {
            "date" : pd.Timestamp("2014-11-19T12:45:00"),
            "usdvalue" : -102300.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ14",
                "dbid" : 4777,
                "hash" : 100004777
            },
            "qty" : -1.0,
            "price" : 2046.0
        },
        {
            "date" : pd.Timestamp("2014-11-19T12:45:00"),
            "usdvalue" : -7052.63042472675,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1419050",
                "dbid" : 11604259,
                "hash" : 211604259
            },
            "qty" : -1.0,
            "price" : 141.052608494535
        },
        {
            "date" : pd.Timestamp("2014-11-19T12:45:00"),
            "usdvalue" : -0.23667239656065,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1418350",
                "dbid" : 11604477,
                "hash" : 211604477
            },
            "qty" : -1.0,
            "price" : 0.004733447931213
        },
        {
            "date" : pd.Timestamp("2014-11-19T12:45:00"),
            "usdvalue" : 8051.59030149481,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1418850",
                "dbid" : 11604255,
                "hash" : 211604255
            },
            "qty" : 1.0,
            "price" : 161.031806029896
        },
        {
            "date" : pd.Timestamp("2014-11-19T12:45:00"),
            "usdvalue" : 902.996503946457,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1420200",
                "dbid" : 11536577,
                "hash" : 211536577
            },
            "qty" : 1.0,
            "price" : 18.0599300789291
        },
        {
            "date" : pd.Timestamp("2014-11-19T12:45:00"),
            "usdvalue" : 102300.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ14",
                "dbid" : 4777,
                "hash" : 100004777
            },
            "qty" : 1.0,
            "price" : 2046.0
        },
        {
            "date" : pd.Timestamp("2014-11-19T12:45:00"),
            "usdvalue" : -723.295142661357,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1420700",
                "dbid" : 11535819,
                "hash" : 211535819
            },
            "qty" : -1.0,
            "price" : 14.4659028532271
        },
        {
            "date" : pd.Timestamp("2014-11-19T12:45:00"),
            "usdvalue" : 388.500572511313,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1420900",
                "dbid" : 11535822,
                "hash" : 211535822
            },
            "qty" : 1.0,
            "price" : 7.77001145022626
        },
        {
            "date" : pd.Timestamp("2014-12-17T12:45:00"),
            "usdvalue" : -851.799362681527,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1420200",
                "dbid" : 11536577,
                "hash" : 211536577
            },
            "qty" : -1.0,
            "price" : 17.0359872536305
        },
        {
            "date" : pd.Timestamp("2014-12-17T12:45:00"),
            "usdvalue" : 67.1334697037551,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1420700",
                "dbid" : 11535819,
                "hash" : 211535819
            },
            "qty" : 1.0,
            "price" : 1.3426693940751
        },
        {
            "date" : pd.Timestamp("2014-12-17T12:45:00"),
            "usdvalue" : -31.0920798561391,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1420900",
                "dbid" : 11535822,
                "hash" : 211535822
            },
            "qty" : -1.0,
            "price" : 0.621841597122781
        },
        {
            "date" : pd.Timestamp("2014-12-17T12:45:00"),
            "usdvalue" : -100662.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ14",
                "dbid" : 4777,
                "hash" : 100004777
            },
            "qty" : -1.0,
            "price" : 2013.25
        },
        {
            "date" : pd.Timestamp("2014-12-17T12:45:00"),
            "usdvalue" : 1540.50887623452,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1519800",
                "dbid" : 11610619,
                "hash" : 211610619
            },
            "qty" : 1.0,
            "price" : 30.8101775246904
        },
        {
            "date" : pd.Timestamp("2014-12-17T12:45:00"),
            "usdvalue" : 100375.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH15",
                "dbid" : 4803,
                "hash" : 100004803
            },
            "qty" : 1.0,
            "price" : 2007.5
        },
        {
            "date" : pd.Timestamp("2014-12-17T12:45:00"),
            "usdvalue" : -1403.58471670174,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1520300",
                "dbid" : 11610442,
                "hash" : 211610442
            },
            "qty" : -1.0,
            "price" : 28.0716943340349
        },
        {
            "date" : pd.Timestamp("2014-12-17T12:45:00"),
            "usdvalue" : 966.943737911555,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1520500",
                "dbid" : 11610444,
                "hash" : 211610444
            },
            "qty" : 1.0,
            "price" : 19.3388747582311
        },
        {
            "date" : pd.Timestamp("2015-01-14T12:45:00"),
            "usdvalue" : 181.313519997951,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1520300",
                "dbid" : 11610442,
                "hash" : 211610442
            },
            "qty" : 1.0,
            "price" : 3.62627039995903
        },
        {
            "date" : pd.Timestamp("2015-01-14T12:45:00"),
            "usdvalue" : -243.631410439875,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1519800",
                "dbid" : 11610619,
                "hash" : 211610619
            },
            "qty" : -1.0,
            "price" : 4.87262820879749
        },
        {
            "date" : pd.Timestamp("2015-01-14T12:45:00"),
            "usdvalue" : -37.1093594032693,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1520500",
                "dbid" : 11610444,
                "hash" : 211610444
            },
            "qty" : -1.0,
            "price" : 0.742187188065387
        },
        {
            "date" : pd.Timestamp("2015-01-14T12:45:00"),
            "usdvalue" : -100287.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH15",
                "dbid" : 4803,
                "hash" : 100004803
            },
            "qty" : -1.0,
            "price" : 2005.75
        },
        {
            "date" : pd.Timestamp("2015-01-14T12:45:00"),
            "usdvalue" : 1798.9978860461,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1519800",
                "dbid" : 11626975,
                "hash" : 211626975
            },
            "qty" : 1.0,
            "price" : 35.9799577209219
        },
        {
            "date" : pd.Timestamp("2015-01-14T12:45:00"),
            "usdvalue" : 100287.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH15",
                "dbid" : 4803,
                "hash" : 100004803
            },
            "qty" : 1.0,
            "price" : 2005.75
        },
        {
            "date" : pd.Timestamp("2015-01-14T12:45:00"),
            "usdvalue" : -1553.8594158549,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1520300",
                "dbid" : 11626749,
                "hash" : 211626749
            },
            "qty" : -1.0,
            "price" : 31.077188317098
        },
        {
            "date" : pd.Timestamp("2015-01-14T12:45:00"),
            "usdvalue" : 1064.68851799436,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1520500",
                "dbid" : 11626753,
                "hash" : 211626753
            },
            "qty" : 1.0,
            "price" : 21.2937703598872
        },
        {
            "date" : pd.Timestamp("2015-02-18T12:45:00"),
            "usdvalue" : -2236.76990390458,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1520500",
                "dbid" : 11626753,
                "hash" : 211626753
            },
            "qty" : -1.0,
            "price" : 44.7353980780915
        },
        {
            "date" : pd.Timestamp("2015-02-18T12:45:00"),
            "usdvalue" : -104700.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH15",
                "dbid" : 4803,
                "hash" : 100004803
            },
            "qty" : -1.0,
            "price" : 2094.0
        },
        {
            "date" : pd.Timestamp("2015-02-18T12:45:00"),
            "usdvalue" : 3215.19390154473,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1520300",
                "dbid" : 11626749,
                "hash" : 211626749
            },
            "qty" : 1.0,
            "price" : 64.3038780308946
        },
        {
            "date" : pd.Timestamp("2015-02-18T12:45:00"),
            "usdvalue" : -3.26557615751133,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1519800",
                "dbid" : 11626975,
                "hash" : 211626975
            },
            "qty" : -1.0,
            "price" : 0.0653115231502266
        },
        {
            "date" : pd.Timestamp("2015-02-18T12:45:00"),
            "usdvalue" : 1198.76459651186,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1520700",
                "dbid" : 11562412,
                "hash" : 211562412
            },
            "qty" : 1.0,
            "price" : 23.9752919302372
        },
        {
            "date" : pd.Timestamp("2015-02-18T12:45:00"),
            "usdvalue" : 104700.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH15",
                "dbid" : 4803,
                "hash" : 100004803
            },
            "qty" : 1.0,
            "price" : 2094.0
        },
        {
            "date" : pd.Timestamp("2015-02-18T12:45:00"),
            "usdvalue" : -896.502424418412,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1521200",
                "dbid" : 11562177,
                "hash" : 211562177
            },
            "qty" : -1.0,
            "price" : 17.9300484883682
        },
        {
            "date" : pd.Timestamp("2015-02-18T12:45:00"),
            "usdvalue" : 497.216654511431,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1521400",
                "dbid" : 11562180,
                "hash" : 211562180
            },
            "qty" : 1.0,
            "price" : 9.94433309022861
        },
        {
            "date" : pd.Timestamp("2015-03-18T12:45:00"),
            "usdvalue" : 126.928498219104,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1521200",
                "dbid" : 11562177,
                "hash" : 211562177
            },
            "qty" : 1.0,
            "price" : 2.53856996438208
        },
        {
            "date" : pd.Timestamp("2015-03-18T12:45:00"),
            "usdvalue" : -116.310610962068,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1520700",
                "dbid" : 11562412,
                "hash" : 211562412
            },
            "qty" : -1.0,
            "price" : 2.32621221924137
        },
        {
            "date" : pd.Timestamp("2015-03-18T12:45:00"),
            "usdvalue" : -30.0898634679456,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1521400",
                "dbid" : 11562180,
                "hash" : 211562180
            },
            "qty" : -1.0,
            "price" : 0.601797269358912
        },
        {
            "date" : pd.Timestamp("2015-03-18T12:45:00"),
            "usdvalue" : -104950.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPH15",
                "dbid" : 4803,
                "hash" : 100004803
            },
            "qty" : -1.0,
            "price" : 2099.0
        },
        {
            "date" : pd.Timestamp("2015-03-18T12:45:00"),
            "usdvalue" : 1119.62066002921,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1520650",
                "dbid" : 11643219,
                "hash" : 211643219
            },
            "qty" : 1.0,
            "price" : 22.3924132005842
        },
        {
            "date" : pd.Timestamp("2015-03-18T12:45:00"),
            "usdvalue" : 104550.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM15",
                "dbid" : 5022,
                "hash" : 100005022
            },
            "qty" : 1.0,
            "price" : 2091.0
        },
        {
            "date" : pd.Timestamp("2015-03-18T12:45:00"),
            "usdvalue" : -916.305874417424,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1521150",
                "dbid" : 11643148,
                "hash" : 211643148
            },
            "qty" : -1.0,
            "price" : 18.3261174883485
        },
        {
            "date" : pd.Timestamp("2015-03-18T12:45:00"),
            "usdvalue" : 525.00255513574,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1521350",
                "dbid" : 11643149,
                "hash" : 211643149
            },
            "qty" : 1.0,
            "price" : 10.5000511027148
        },
        {
            "date" : pd.Timestamp("2015-04-15T12:45:00"),
            "usdvalue" : -26.9118668147328,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1520650",
                "dbid" : 11643219,
                "hash" : 211643219
            },
            "qty" : -1.0,
            "price" : 0.538237336294657
        },
        {
            "date" : pd.Timestamp("2015-04-15T12:45:00"),
            "usdvalue" : 68.5414632271488,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1521150",
                "dbid" : 11643148,
                "hash" : 211643148
            },
            "qty" : 1.0,
            "price" : 1.37082926454298
        },
        {
            "date" : pd.Timestamp("2015-04-15T12:45:00"),
            "usdvalue" : -7.07187530701638,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1521350",
                "dbid" : 11643149,
                "hash" : 211643149
            },
            "qty" : -1.0,
            "price" : 0.141437506140328
        },
        {
            "date" : pd.Timestamp("2015-04-15T12:45:00"),
            "usdvalue" : -104987.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM15",
                "dbid" : 5022,
                "hash" : 100005022
            },
            "qty" : -1.0,
            "price" : 2099.75
        },
        {
            "date" : pd.Timestamp("2015-04-15T12:45:00"),
            "usdvalue" : 1008.68749353679,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1520750",
                "dbid" : 11684341,
                "hash" : 211684341
            },
            "qty" : 1.0,
            "price" : 20.1737498707358
        },
        {
            "date" : pd.Timestamp("2015-04-15T12:45:00"),
            "usdvalue" : 104987.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM15",
                "dbid" : 5022,
                "hash" : 100005022
            },
            "qty" : 1.0,
            "price" : 2099.75
        },
        {
            "date" : pd.Timestamp("2015-04-15T12:45:00"),
            "usdvalue" : -747.058610772837,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1521250",
                "dbid" : 11684111,
                "hash" : 211684111
            },
            "qty" : -1.0,
            "price" : 14.9411722154567
        },
        {
            "date" : pd.Timestamp("2015-04-15T12:45:00"),
            "usdvalue" : 388.908675272305,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1521450",
                "dbid" : 11684115,
                "hash" : 211684115
            },
            "qty" : 1.0,
            "price" : 7.77817350544609
        },
        {
            "date" : pd.Timestamp("2015-05-13T12:45:00"),
            "usdvalue" : -1.41442237360367,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1521450",
                "dbid" : 11684115,
                "hash" : 211684115
            },
            "qty" : -1.0,
            "price" : 0.0282884474720735
        },
        {
            "date" : pd.Timestamp("2015-05-13T12:45:00"),
            "usdvalue" : -176.96056681483,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1520750",
                "dbid" : 11684341,
                "hash" : 211684341
            },
            "qty" : -1.0,
            "price" : 3.5392113362966
        },
        {
            "date" : pd.Timestamp("2015-05-13T12:45:00"),
            "usdvalue" : -104725.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM15",
                "dbid" : 5022,
                "hash" : 100005022
            },
            "qty" : -1.0,
            "price" : 2094.5
        },
        {
            "date" : pd.Timestamp("2015-05-13T12:45:00"),
            "usdvalue" : 17.1188021173286,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1521250",
                "dbid" : 11684111,
                "hash" : 211684111
            },
            "qty" : 1.0,
            "price" : 0.342376042346572
        },
        {
            "date" : pd.Timestamp("2015-05-13T12:45:00"),
            "usdvalue" : 1276.21978581349,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1520700",
                "dbid" : 11599146,
                "hash" : 211599146
            },
            "qty" : 1.0,
            "price" : 25.5243957162697
        },
        {
            "date" : pd.Timestamp("2015-05-13T12:45:00"),
            "usdvalue" : 104725.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM15",
                "dbid" : 5022,
                "hash" : 100005022
            },
            "qty" : 1.0,
            "price" : 2094.5
        },
        {
            "date" : pd.Timestamp("2015-05-13T12:45:00"),
            "usdvalue" : -990.465139116225,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1521200",
                "dbid" : 11598975,
                "hash" : 211598975
            },
            "qty" : -1.0,
            "price" : 19.8093027823245
        },
        {
            "date" : pd.Timestamp("2015-05-13T12:45:00"),
            "usdvalue" : 572.249539017088,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1521400",
                "dbid" : 11598978,
                "hash" : 211598978
            },
            "qty" : 1.0,
            "price" : 11.4449907803418
        },
        {
            "date" : pd.Timestamp("2015-06-17T12:45:00"),
            "usdvalue" : -17.3001208448802,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1521400",
                "dbid" : 11598978,
                "hash" : 211598978
            },
            "qty" : -1.0,
            "price" : 0.346002416897605
        },
        {
            "date" : pd.Timestamp("2015-06-17T12:45:00"),
            "usdvalue" : -98.6482034312758,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1520700",
                "dbid" : 11599146,
                "hash" : 211599146
            },
            "qty" : -1.0,
            "price" : 1.97296406862552
        },
        {
            "date" : pd.Timestamp("2015-06-17T12:45:00"),
            "usdvalue" : -105062.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPM15",
                "dbid" : 5022,
                "hash" : 100005022
            },
            "qty" : -1.0,
            "price" : 2101.25
        },
        {
            "date" : pd.Timestamp("2015-06-17T12:45:00"),
            "usdvalue" : 127.766344768682,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1521200",
                "dbid" : 11598975,
                "hash" : 211598975
            },
            "qty" : 1.0,
            "price" : 2.55532689537364
        },
        {
            "date" : pd.Timestamp("2015-06-17T12:45:00"),
            "usdvalue" : 1189.38315824649,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1520700",
                "dbid" : 11696243,
                "hash" : 211696243
            },
            "qty" : 1.0,
            "price" : 23.7876631649298
        },
        {
            "date" : pd.Timestamp("2015-06-17T12:45:00"),
            "usdvalue" : 104637.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU15",
                "dbid" : 5161,
                "hash" : 100005161
            },
            "qty" : 1.0,
            "price" : 2092.75
        },
        {
            "date" : pd.Timestamp("2015-06-17T12:45:00"),
            "usdvalue" : -828.948960909196,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1521200",
                "dbid" : 11696040,
                "hash" : 211696040
            },
            "qty" : -1.0,
            "price" : 16.5789792181839
        },
        {
            "date" : pd.Timestamp("2015-06-17T12:45:00"),
            "usdvalue" : 447.348177326029,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1521400",
                "dbid" : 11696043,
                "hash" : 211696043
            },
            "qty" : 1.0,
            "price" : 8.94696354652058
        },
        {
            "date" : pd.Timestamp("2015-07-15T12:45:00"),
            "usdvalue" : 27.4078159149809,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1521200",
                "dbid" : 11696040,
                "hash" : 211696040
            },
            "qty" : 1.0,
            "price" : 0.548156318299618
        },
        {
            "date" : pd.Timestamp("2015-07-15T12:45:00"),
            "usdvalue" : -104937.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU15",
                "dbid" : 5161,
                "hash" : 100005161
            },
            "qty" : -1.0,
            "price" : 2098.75
        },
        {
            "date" : pd.Timestamp("2015-07-15T12:45:00"),
            "usdvalue" : -2.31229879456336,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPN1521400",
                "dbid" : 11696043,
                "hash" : 211696043
            },
            "qty" : -1.0,
            "price" : 0.0462459758912672
        },
        {
            "date" : pd.Timestamp("2015-07-15T12:45:00"),
            "usdvalue" : -74.7744091128041,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPN1520700",
                "dbid" : 11696243,
                "hash" : 211696243
            },
            "qty" : -1.0,
            "price" : 1.49548818225608
        },
        {
            "date" : pd.Timestamp("2015-07-15T12:45:00"),
            "usdvalue" : 1200.91769693321,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1520750",
                "dbid" : 11707239,
                "hash" : 211707239
            },
            "qty" : 1.0,
            "price" : 24.0183539386643
        },
        {
            "date" : pd.Timestamp("2015-07-15T12:45:00"),
            "usdvalue" : 104937.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU15",
                "dbid" : 5161,
                "hash" : 100005161
            },
            "qty" : 1.0,
            "price" : 2098.75
        },
        {
            "date" : pd.Timestamp("2015-07-15T12:45:00"),
            "usdvalue" : -878.264120997369,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1521250",
                "dbid" : 11707015,
                "hash" : 211707015
            },
            "qty" : -1.0,
            "price" : 17.5652824199474
        },
        {
            "date" : pd.Timestamp("2015-07-15T12:45:00"),
            "usdvalue" : 472.425865487173,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1521450",
                "dbid" : 11707019,
                "hash" : 211707019
            },
            "qty" : 1.0,
            "price" : 9.44851730974347
        },
        {
            "date" : pd.Timestamp("2015-08-19T12:45:00"),
            "usdvalue" : -104112.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU15",
                "dbid" : 5161,
                "hash" : 100005161
            },
            "qty" : -1.0,
            "price" : 2082.25
        },
        {
            "date" : pd.Timestamp("2015-08-19T12:45:00"),
            "usdvalue" : -285.392393765272,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPQ1520750",
                "dbid" : 11707239,
                "hash" : 211707239
            },
            "qty" : -1.0,
            "price" : 5.70784787530545
        },
        {
            "date" : pd.Timestamp("2015-08-19T12:45:00"),
            "usdvalue" : -0.0240677627012617,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1521450",
                "dbid" : 11707019,
                "hash" : 211707019
            },
            "qty" : -1.0,
            "price" : 0.000481355254025234
        },
        {
            "date" : pd.Timestamp("2015-08-19T12:45:00"),
            "usdvalue" : 0.352066934214856,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPQ1521250",
                "dbid" : 11707015,
                "hash" : 211707015
            },
            "qty" : 1.0,
            "price" : 0.00704133868429713
        },
        {
            "date" : pd.Timestamp("2015-08-19T12:45:00"),
            "usdvalue" : 1087.22792715278,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1520550",
                "dbid" : 11700251,
                "hash" : 211700251
            },
            "qty" : 1.0,
            "price" : 21.7445585430555
        },
        {
            "date" : pd.Timestamp("2015-08-19T12:45:00"),
            "usdvalue" : 104112.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU15",
                "dbid" : 5161,
                "hash" : 100005161
            },
            "qty" : 1.0,
            "price" : 2082.25
        },
        {
            "date" : pd.Timestamp("2015-08-19T12:45:00"),
            "usdvalue" : -891.356180614872,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1521050",
                "dbid" : 11700191,
                "hash" : 211700191
            },
            "qty" : -1.0,
            "price" : 17.8271236122974
        },
        {
            "date" : pd.Timestamp("2015-08-19T12:45:00"),
            "usdvalue" : 473.535329221471,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1521250",
                "dbid" : 11617231,
                "hash" : 211617231
            },
            "qty" : 1.0,
            "price" : 9.47070658442942
        },
        {
            "date" : pd.Timestamp("2015-09-16T12:45:00"),
            "usdvalue" : -99737.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPU15",
                "dbid" : 5161,
                "hash" : 100005161
            },
            "qty" : -1.0,
            "price" : 1994.75
        },
        {
            "date" : pd.Timestamp("2015-09-16T12:45:00"),
            "usdvalue" : -3027.47529918901,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1520550",
                "dbid" : 11700251,
                "hash" : 211700251
            },
            "qty" : -1.0,
            "price" : 60.5495059837801
        },
        {
            "date" : pd.Timestamp("2015-09-16T12:45:00"),
            "usdvalue" : -0.859035645853012,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1521250",
                "dbid" : 11617231,
                "hash" : 211617231
            },
            "qty" : -1.0,
            "price" : 0.0171807129170602
        },
        {
            "date" : pd.Timestamp("2015-09-16T12:45:00"),
            "usdvalue" : 1.05644228903596,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1521050",
                "dbid" : 11700191,
                "hash" : 211700191
            },
            "qty" : 1.0,
            "price" : 0.0211288457807193
        },
        {
            "date" : pd.Timestamp("2015-09-16T12:45:00"),
            "usdvalue" : 1723.86244221547,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1519600",
                "dbid" : 11713069,
                "hash" : 211713069
            },
            "qty" : 1.0,
            "price" : 34.4772488443093
        },
        {
            "date" : pd.Timestamp("2015-09-16T12:45:00"),
            "usdvalue" : 99225.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ15",
                "dbid" : 5265,
                "hash" : 100005265
            },
            "qty" : 1.0,
            "price" : 1984.5
        },
        {
            "date" : pd.Timestamp("2015-09-16T12:45:00"),
            "usdvalue" : -1427.19312334127,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1520100",
                "dbid" : 11712868,
                "hash" : 211712868
            },
            "qty" : -1.0,
            "price" : 28.5438624668254
        },
        {
            "date" : pd.Timestamp("2015-09-16T12:45:00"),
            "usdvalue" : 965.520261804272,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1520300",
                "dbid" : 11712871,
                "hash" : 211712871
            },
            "qty" : 1.0,
            "price" : 19.3104052360854
        },
        {
            "date" : pd.Timestamp("2015-10-14T12:45:00"),
            "usdvalue" : -99312.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ15",
                "dbid" : 5265,
                "hash" : 100005265
            },
            "qty" : -1.0,
            "price" : 1986.25
        },
        {
            "date" : pd.Timestamp("2015-10-14T12:45:00"),
            "usdvalue" : 76.2157724570329,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1520100",
                "dbid" : 11712868,
                "hash" : 211712868
            },
            "qty" : 1.0,
            "price" : 1.52431544914066
        },
        {
            "date" : pd.Timestamp("2015-10-14T12:45:00"),
            "usdvalue" : -146.877301829173,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPV1519600",
                "dbid" : 11713069,
                "hash" : 211713069
            },
            "qty" : -1.0,
            "price" : 2.93754603658346
        },
        {
            "date" : pd.Timestamp("2015-10-14T12:45:00"),
            "usdvalue" : -6.56506430275066,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPV1520300",
                "dbid" : 11712871,
                "hash" : 211712871
            },
            "qty" : -1.0,
            "price" : 0.131301286055013
        },
        {
            "date" : pd.Timestamp("2015-10-14T12:45:00"),
            "usdvalue" : 1552.36121351161,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1519600",
                "dbid" : 11723195,
                "hash" : 211723195
            },
            "qty" : 1.0,
            "price" : 31.0472242702322
        },
        {
            "date" : pd.Timestamp("2015-10-14T12:45:00"),
            "usdvalue" : 99312.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ15",
                "dbid" : 5265,
                "hash" : 100005265
            },
            "qty" : 1.0,
            "price" : 1986.25
        },
        {
            "date" : pd.Timestamp("2015-10-14T12:45:00"),
            "usdvalue" : -1336.35791844276,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1520100",
                "dbid" : 11722968,
                "hash" : 211722968
            },
            "qty" : -1.0,
            "price" : 26.7271583688552
        },
        {
            "date" : pd.Timestamp("2015-10-14T12:45:00"),
            "usdvalue" : 888.969242493761,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1520300",
                "dbid" : 11722972,
                "hash" : 211722972
            },
            "qty" : 1.0,
            "price" : 17.7793848498752
        },
        {
            "date" : pd.Timestamp("2015-11-18T12:45:00"),
            "usdvalue" : 3402.13463350992,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1520100",
                "dbid" : 11722968,
                "hash" : 211722968
            },
            "qty" : 1.0,
            "price" : 68.0426926701984
        },
        {
            "date" : pd.Timestamp("2015-11-18T12:45:00"),
            "usdvalue" : -103887.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ15",
                "dbid" : 5265,
                "hash" : 100005265
            },
            "qty" : -1.0,
            "price" : 2077.75
        },
        {
            "date" : pd.Timestamp("2015-11-18T12:45:00"),
            "usdvalue" : -1.80453941203611,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPX1519600",
                "dbid" : 11723195,
                "hash" : 211723195
            },
            "qty" : -1.0,
            "price" : 0.0360907882407222
        },
        {
            "date" : pd.Timestamp("2015-11-18T12:45:00"),
            "usdvalue" : -2426.19134963293,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPX1520300",
                "dbid" : 11722972,
                "hash" : 211722972
            },
            "qty" : -1.0,
            "price" : 48.5238269926585
        },
        {
            "date" : pd.Timestamp("2015-11-18T12:45:00"),
            "usdvalue" : 1373.4751456397,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1520550",
                "dbid" : 11716905,
                "hash" : 211716905
            },
            "qty" : 1.0,
            "price" : 27.4695029127939
        },
        {
            "date" : pd.Timestamp("2015-11-18T12:45:00"),
            "usdvalue" : 103887.5,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ15",
                "dbid" : 5265,
                "hash" : 100005265
            },
            "qty" : 1.0,
            "price" : 2077.75
        },
        {
            "date" : pd.Timestamp("2015-11-18T12:45:00"),
            "usdvalue" : -1034.37254125038,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1521050",
                "dbid" : 11716838,
                "hash" : 211716838
            },
            "qty" : -1.0,
            "price" : 20.6874508250077
        },
        {
            "date" : pd.Timestamp("2015-11-18T12:45:00"),
            "usdvalue" : 646.357631339151,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1521250",
                "dbid" : 11643940,
                "hash" : 211643940
            },
            "qty" : 1.0,
            "price" : 12.927152626783
        },
        {
            "date" : pd.Timestamp("2015-12-16T12:45:00"),
            "usdvalue" : -390.469597903422,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1520550",
                "dbid" : 11716905,
                "hash" : 211716905
            },
            "qty" : -1.0,
            "price" : 7.80939195806843
        },
        {
            "date" : pd.Timestamp("2015-12-16T12:45:00"),
            "usdvalue" : -52.1006984757918,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1521250",
                "dbid" : 11643940,
                "hash" : 211643940
            },
            "qty" : -1.0,
            "price" : 1.04201396951584
        },
        {
            "date" : pd.Timestamp("2015-12-16T12:45:00"),
            "usdvalue" : 177.449044812056,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1521050",
                "dbid" : 11716838,
                "hash" : 211716838
            },
            "qty" : 1.0,
            "price" : 3.54898089624112
        },
        {
            "date" : pd.Timestamp("2015-12-16T12:45:00"),
            "usdvalue" : -103775.0,
            "asset" : {
                "type" : "F",
                "name" : "F.US.EPZ15",
                "dbid" : 5265,
                "hash" : 100005265
            },
            "qty" : -1.0,
            "price" : 2075.5
        },
        {
            "date" : pd.Timestamp("2015-12-16T12:45:00"),
            "usdvalue" : 1458.89576432913,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1620400",
                "dbid" : 11730638,
                "hash" : 211730638
            },
            "qty" : 1.0,
            "price" : 29.1779152865827
        },
        {
            "date" : pd.Timestamp("2015-12-16T12:45:00"),
            "usdvalue" : 103375.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPH16",
                "dbid" : 5546,
                "hash" : 100005546
            },
            "qty" : 1.0,
            "price" : 2067.5
        },
        {
            "date" : pd.Timestamp("2015-12-16T12:45:00"),
            "usdvalue" : -1317.76690167192,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1620900",
                "dbid" : 11730442,
                "hash" : 211730442
            },
            "qty" : -1.0,
            "price" : 26.3553380334384
        },
        {
            "date" : pd.Timestamp("2015-12-16T12:45:00"),
            "usdvalue" : 866.516127998585,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1621100",
                "dbid" : 11730444,
                "hash" : 211730444
            },
            "qty" : 1.0,
            "price" : 17.3303225599717
        },
        {
            "date" : pd.Timestamp("2016-01-13T12:45:00"),
            "usdvalue" : -94325.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPH16",
                "dbid" : 5546,
                "hash" : 100005546
            },
            "qty" : -1.0,
            "price" : 1886.5
        },
        {
            "date" : pd.Timestamp("2016-01-13T12:45:00"),
            "usdvalue" : -0.00847047620084231,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1621100",
                "dbid" : 11730444,
                "hash" : 211730444
            },
            "qty" : -1.0,
            "price" : 0.000169409524016846
        },
        {
            "date" : pd.Timestamp("2016-01-13T12:45:00"),
            "usdvalue" : 0.00629306491104781,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPF1620900",
                "dbid" : 11730442,
                "hash" : 211730442
            },
            "qty" : 1.0,
            "price" : 0.000125861298220956
        },
        {
            "date" : pd.Timestamp("2016-01-13T12:45:00"),
            "usdvalue" : -7671.13878550913,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPF1620400",
                "dbid" : 11730638,
                "hash" : 211730638
            },
            "qty" : -1.0,
            "price" : 153.422775710183
        },
        {
            "date" : pd.Timestamp("2016-01-13T12:45:00"),
            "usdvalue" : 1983.12729705798,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1618600",
                "dbid" : 11739450,
                "hash" : 211739450
            },
            "qty" : 1.0,
            "price" : 39.6625459411596
        },
        {
            "date" : pd.Timestamp("2016-01-13T12:45:00"),
            "usdvalue" : 94325.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPH16",
                "dbid" : 5546,
                "hash" : 100005546
            },
            "qty" : 1.0,
            "price" : 1886.5
        },
        {
            "date" : pd.Timestamp("2016-01-13T12:45:00"),
            "usdvalue" : -1837.95374814595,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1619100",
                "dbid" : 11738931,
                "hash" : 211738931
            },
            "qty" : -1.0,
            "price" : 36.7590749629189
        },
        {
            "date" : pd.Timestamp("2016-01-13T12:45:00"),
            "usdvalue" : 1377.31737591805,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1619300",
                "dbid" : 11738935,
                "hash" : 211738935
            },
            "qty" : 1.0,
            "price" : 27.546347518361
        },
        {
            "date" : pd.Timestamp("2016-02-17T12:45:00"),
            "usdvalue" : -96187.5,
            "asset" : {
                "type" : "F",
                "name" : "F.EPH16",
                "dbid" : 5546,
                "hash" : 100005546
            },
            "qty" : -1.0,
            "price" : 1923.75
        },
        {
            "date" : pd.Timestamp("2016-02-17T12:45:00"),
            "usdvalue" : 942.191512472561,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1619100",
                "dbid" : 11738931,
                "hash" : 211738931
            },
            "qty" : 1.0,
            "price" : 18.8438302494512
        },
        {
            "date" : pd.Timestamp("2016-02-17T12:45:00"),
            "usdvalue" : -14.9746676128832,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPG1618600",
                "dbid" : 11739450,
                "hash" : 211739450
            },
            "qty" : -1.0,
            "price" : 0.299493352257663
        },
        {
            "date" : pd.Timestamp("2016-02-17T12:45:00"),
            "usdvalue" : -361.412489928483,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPG1619300",
                "dbid" : 11738935,
                "hash" : 211738935
            },
            "qty" : -1.0,
            "price" : 7.22824979856966
        },
        {
            "date" : pd.Timestamp("2016-02-17T12:45:00"),
            "usdvalue" : 1758.54608116684,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1619000",
                "dbid" : 11701018,
                "hash" : 211701018
            },
            "qty" : 1.0,
            "price" : 35.1709216233369
        },
        {
            "date" : pd.Timestamp("2016-02-17T12:45:00"),
            "usdvalue" : 96187.5,
            "asset" : {
                "type" : "F",
                "name" : "F.EPH16",
                "dbid" : 5546,
                "hash" : 100005546
            },
            "qty" : 1.0,
            "price" : 1923.75
        },
        {
            "date" : pd.Timestamp("2016-02-17T12:45:00"),
            "usdvalue" : -1503.15629395106,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1619500",
                "dbid" : 11700839,
                "hash" : 211700839
            },
            "qty" : -1.0,
            "price" : 30.0631258790212
        },
        {
            "date" : pd.Timestamp("2016-02-17T12:45:00"),
            "usdvalue" : 1046.02722971093,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1619700",
                "dbid" : 11700841,
                "hash" : 211700841
            },
            "qty" : 1.0,
            "price" : 20.9205445942187
        },
        {
            "date" : pd.Timestamp("2016-03-16T12:45:00"),
            "usdvalue" : -3016.22208243364,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1619700",
                "dbid" : 11700841,
                "hash" : 211700841
            },
            "qty" : -1.0,
            "price" : 60.3244416486727
        },
        {
            "date" : pd.Timestamp("2016-03-16T12:45:00"),
            "usdvalue" : -1.28858838501573,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPH1619000",
                "dbid" : 11701018,
                "hash" : 211701018
            },
            "qty" : -1.0,
            "price" : 0.0257717677003146
        },
        {
            "date" : pd.Timestamp("2016-03-16T12:45:00"),
            "usdvalue" : -101500.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPH16",
                "dbid" : 5546,
                "hash" : 100005546
            },
            "qty" : -1.0,
            "price" : 2030.0
        },
        {
            "date" : pd.Timestamp("2016-03-16T12:45:00"),
            "usdvalue" : 4007.77191574062,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPH1619500",
                "dbid" : 11700839,
                "hash" : 211700839
            },
            "qty" : 1.0,
            "price" : 80.1554383148125
        },
        {
            "date" : pd.Timestamp("2016-03-16T12:45:00"),
            "usdvalue" : 1192.06689091956,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1619950",
                "dbid" : 11739723,
                "hash" : 211739723
            },
            "qty" : 1.0,
            "price" : 23.8413378183913
        },
        {
            "date" : pd.Timestamp("2016-03-16T12:45:00"),
            "usdvalue" : 101000.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPM16",
                "dbid" : 5700,
                "hash" : 100005700
            },
            "qty" : 1.0,
            "price" : 2020.0
        },
        {
            "date" : pd.Timestamp("2016-03-16T12:45:00"),
            "usdvalue" : -958.620783166197,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1620450",
                "dbid" : 11739204,
                "hash" : 211739204
            },
            "qty" : -1.0,
            "price" : 19.1724156633239
        },
        {
            "date" : pd.Timestamp("2016-03-16T12:45:00"),
            "usdvalue" : 560.954534119537,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1620650",
                "dbid" : 11739208,
                "hash" : 211739208
            },
            "qty" : 1.0,
            "price" : 11.2190906823907
        },
        {
            "date" : pd.Timestamp("2016-04-13T12:45:00"),
            "usdvalue" : -690.719802367732,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1620650",
                "dbid" : 11739208,
                "hash" : 211739208
            },
            "qty" : -1.0,
            "price" : 13.8143960473546
        },
        {
            "date" : pd.Timestamp("2016-04-13T12:45:00"),
            "usdvalue" : 1562.62853366982,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPJ1620450",
                "dbid" : 11739204,
                "hash" : 211739204
            },
            "qty" : 1.0,
            "price" : 31.2525706733963
        },
        {
            "date" : pd.Timestamp("2016-04-13T12:45:00"),
            "usdvalue" : -1.32283056925582,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPJ1619950",
                "dbid" : 11739723,
                "hash" : 211739723
            },
            "qty" : -1.0,
            "price" : 0.0264566113851163
        },
        {
            "date" : pd.Timestamp("2016-04-13T12:45:00"),
            "usdvalue" : -103775.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPM16",
                "dbid" : 5700,
                "hash" : 100005700
            },
            "qty" : -1.0,
            "price" : 2075.5
        },
        {
            "date" : pd.Timestamp("2016-04-13T12:45:00"),
            "usdvalue" : 1209.35390880501,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1620500",
                "dbid" : 11755982,
                "hash" : 211755982
            },
            "qty" : 1.0,
            "price" : 24.1870781761003
        },
        {
            "date" : pd.Timestamp("2016-04-13T12:45:00"),
            "usdvalue" : 103775.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPM16",
                "dbid" : 5700,
                "hash" : 100005700
            },
            "qty" : 1.0,
            "price" : 2075.5
        },
        {
            "date" : pd.Timestamp("2016-04-13T12:45:00"),
            "usdvalue" : -952.131170230797,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1621000",
                "dbid" : 11755757,
                "hash" : 211755757
            },
            "qty" : -1.0,
            "price" : 19.0426234046159
        },
        {
            "date" : pd.Timestamp("2016-04-13T12:45:00"),
            "usdvalue" : 525.029819571449,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1621200",
                "dbid" : 11755761,
                "hash" : 211755761
            },
            "qty" : 1.0,
            "price" : 10.500596391429
        },
        {
            "date" : pd.Timestamp("2016-05-18T12:45:00"),
            "usdvalue" : -0.459770418459815,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1621200",
                "dbid" : 11755761,
                "hash" : 211755761
            },
            "qty" : -1.0,
            "price" : 0.0091954083691963
        },
        {
            "date" : pd.Timestamp("2016-05-18T12:45:00"),
            "usdvalue" : -102000.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPM16",
                "dbid" : 5700,
                "hash" : 100005700
            },
            "qty" : -1.0,
            "price" : 2040.0
        },
        {
            "date" : pd.Timestamp("2016-05-18T12:45:00"),
            "usdvalue" : 1.27016900902572,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPK1621000",
                "dbid" : 11755757,
                "hash" : 211755757
            },
            "qty" : 1.0,
            "price" : 0.0254033801805145
        },
        {
            "date" : pd.Timestamp("2016-05-18T12:45:00"),
            "usdvalue" : -753.901233258159,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPK1620500",
                "dbid" : 11755982,
                "hash" : 211755982
            },
            "qty" : -1.0,
            "price" : 15.0780246651632
        },
        {
            "date" : pd.Timestamp("2016-05-18T12:45:00"),
            "usdvalue" : 1194.50683057306,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1620150",
                "dbid" : 11739854,
                "hash" : 211739854
            },
            "qty" : 1.0,
            "price" : 23.8901366114611
        },
        {
            "date" : pd.Timestamp("2016-05-18T12:45:00"),
            "usdvalue" : 102000.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPM16",
                "dbid" : 5700,
                "hash" : 100005700
            },
            "qty" : 1.0,
            "price" : 2040.0
        },
        {
            "date" : pd.Timestamp("2016-05-18T12:45:00"),
            "usdvalue" : -950.709327541432,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1620650",
                "dbid" : 11739329,
                "hash" : 211739329
            },
            "qty" : -1.0,
            "price" : 19.0141865508286
        },
        {
            "date" : pd.Timestamp("2016-05-18T12:45:00"),
            "usdvalue" : 545.540521447839,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1620850",
                "dbid" : 11739330,
                "hash" : 211739330
            },
            "qty" : 1.0,
            "price" : 10.9108104289568
        },
        {
            "date" : pd.Timestamp("2016-06-15T12:45:00"),
            "usdvalue" : 659.134823352474,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1620650",
                "dbid" : 11739329,
                "hash" : 211739329
            },
            "qty" : 1.0,
            "price" : 13.1826964670495
        },
        {
            "date" : pd.Timestamp("2016-06-15T12:45:00"),
            "usdvalue" : -162.386342568374,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPM1620850",
                "dbid" : 11739330,
                "hash" : 211739330
            },
            "qty" : -1.0,
            "price" : 3.24772685136747
        },
        {
            "date" : pd.Timestamp("2016-06-15T12:45:00"),
            "usdvalue" : -103625.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPM16",
                "dbid" : 5700,
                "hash" : 100005700
            },
            "qty" : -1.0,
            "price" : 2072.5
        },
        {
            "date" : pd.Timestamp("2016-06-15T12:45:00"),
            "usdvalue" : -21.6277045398364,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPM1620150",
                "dbid" : 11739854,
                "hash" : 211739854
            },
            "qty" : -1.0,
            "price" : 0.432554090796728
        },
        {
            "date" : pd.Timestamp("2016-06-15T12:45:00"),
            "usdvalue" : 3190.48910344514,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1620400",
                "dbid" : 3148145,
                "hash" : 203148145
            },
            "qty" : 1.0,
            "price" : 63.8097820689028
        },
        {
            "date" : pd.Timestamp("2016-06-15T12:45:00"),
            "usdvalue" : 103212.5,
            "asset" : {
                "type" : "F",
                "name" : "F.EPU16",
                "dbid" : 5951,
                "hash" : 100005951
            },
            "qty" : 1.0,
            "price" : 2064.25
        },
        {
            "date" : pd.Timestamp("2016-06-15T12:45:00"),
            "usdvalue" : -2822.85428366023,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1620900",
                "dbid" : 3147245,
                "hash" : 203147245
            },
            "qty" : -1.0,
            "price" : 56.4570856732047
        },
        {
            "date" : pd.Timestamp("2016-06-15T12:45:00"),
            "usdvalue" : 2268.21872321694,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1621100",
                "dbid" : 3147248,
                "hash" : 203147248
            },
            "qty" : 1.0,
            "price" : 45.3643744643388
        },
        {
            "date" : pd.Timestamp("2016-09-14T12:45:00"),
            "usdvalue" : -1052.63455518598,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1621100",
                "dbid" : 3147248,
                "hash" : 203147248
            },
            "qty" : -1.0,
            "price" : 21.0526911037196
        },
        {
            "date" : pd.Timestamp("2016-09-14T12:45:00"),
            "usdvalue" : -11.2379422478952,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPU1620400",
                "dbid" : 3148145,
                "hash" : 203148145
            },
            "qty" : -1.0,
            "price" : 0.224758844957904
        },
        {
            "date" : pd.Timestamp("2016-09-14T12:45:00"),
            "usdvalue" : 1874.03350162029,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPU1620900",
                "dbid" : 3147245,
                "hash" : 203147245
            },
            "qty" : 1.0,
            "price" : 37.4806700324059
        },
        {
            "date" : pd.Timestamp("2016-09-14T12:45:00"),
            "usdvalue" : -106262.5,
            "asset" : {
                "type" : "F",
                "name" : "F.EPU16",
                "dbid" : 5951,
                "hash" : 100005951
            },
            "qty" : -1.0,
            "price" : 2125.25
        },
        {
            "date" : pd.Timestamp("2016-09-14T12:45:00"),
            "usdvalue" : 3013.95208628632,
            "asset" : {
                "type" : "O",
                "name" : "P.US.EPZ1620950",
                "dbid" : 3148813,
                "hash" : 203148813
            },
            "qty" : 1.0,
            "price" : 60.2790417257263
        },
        {
            "date" : pd.Timestamp("2016-09-14T12:45:00"),
            "usdvalue" : 105925.0,
            "asset" : {
                "type" : "F",
                "name" : "F.EPZ16",
                "dbid" : 6570,
                "hash" : 100006570
            },
            "qty" : 1.0,
            "price" : 2118.5
        },
        {
            "date" : pd.Timestamp("2016-09-14T12:45:00"),
            "usdvalue" : -2611.56510629721,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1621450",
                "dbid" : 3147442,
                "hash" : 203147442
            },
            "qty" : -1.0,
            "price" : 52.2313021259441
        },
        {
            "date" : pd.Timestamp("2016-09-14T12:45:00"),
            "usdvalue" : 2067.81315840769,
            "asset" : {
                "type" : "O",
                "name" : "C.US.EPZ1621650",
                "dbid" : 3147944,
                "hash" : 203147944
            },
            "qty" : 1.0,
            "price" : 41.3562631681539
        }
    ],
    "name" : "ES_BullishCollarBW",
    "calc_date" : pd.Timestamp("2016-11-14T12:46:15.835Z"),
    "position" : {
        "positions" : {
            "100006570" : {
                "leg_name" : "fut_leg",
                "qty" : 1.0,
                "value" : 105925.0
            },
            "203147944" : {
                "leg_name" : "call_up9_long_leg",
                "qty" : 1.0,
                "value" : 2067.81315840769
            },
            "203147442" : {
                "leg_name" : "call_up5_short_leg",
                "qty" : -1.0,
                "value" : -2611.56510629721
            },
            "203148813" : {
                "leg_name" : "opt_otm_leg",
                "qty" : 1.0,
                "value" : 3013.95208628632
            }
        },
        "_realized_pnl" : 9897.57852486567
    }
}