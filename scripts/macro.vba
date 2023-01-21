Option Explicit

Public Function HexToRgbLong(hexColor As String) As Long
    Dim R As String
    Dim G As String
    Dim B As String

    R = Val("&H" & Left(hexColor, 2))
    G = Val("&H" & Mid(hexColor, 3, 2))
    B = Val("&H" & Right(hexColor, 2))
 
    HexToRgbLong = B * 65536 + G * 256 + R
End Function

Public Function indexFormula(holomemName As String, colName As String) As String
    ' reference value regardless of position in the table (i.e. when sorting)
    indexFormula = "INDEX(main!A1:O100, MATCH(" & """" & holomemName & """" & ", main!A1:A100, 0), MATCH(" & """" & colName & """" & ", main!A1:O1, 0))"
End Function

Sub main()
    Dim holomemIndex As Integer
    Dim holomemName As String
    Dim noStreamColor As String
    Dim oneStreamColor As String
    Dim mostStreamedColor As String
    Dim rowNum As Integer
    Dim rg As Range
    Dim cs As ColorScale
    Dim co As ChartObject
 
    ' index corresponding to row no. in main worksheet
    For holomemIndex =  2 To 82
        holomemName = Worksheets("main").Cells(holomemIndex, 1)

        ' check if sheet doesn't exist
        If IsError(Evaluate(holomemName & "!A1")) Then
            Worksheets("template").Copy After:=Sheets(Sheets.Count) ' copy template and place at the end
            ActiveSheet.Name = holomemName ' name worksheet
        Else
            Worksheets(holomemName).Activate ' activate existing sheet
        End If

        ' delete all prev conditional formatting to avoid duplicates
        ActiveSheet.Cells.FormatConditions.Delete

        ' copy data from staging worksheet
        With Worksheets("staging")
            .Range("A" & (holomemIndex - 2) * 23 + 2 & ":BCJ" & (holomemIndex - 2) * 23 + 9).Copy ActiveSheet.Range("B4:BCK10") ' heatmap
            .Range("A" & (holomemIndex - 2) * 23 + 11 & ":A" & (holomemIndex - 2) * 23 + 22).Copy ActiveSheet.Range("BCQ51:BCQ62") ' stream duration count
            .Range("C" & (holomemIndex - 2) * 23 + 11 & ":C" & (holomemIndex - 2) * 23 + 17).Copy ActiveSheet.Range("BCT51:BCT57") ' cummulative streams/day
            .Range("E" & (holomemIndex - 2) * 23 + 11 & ":F" & (holomemIndex - 2) * 23 + 20).Copy ActiveSheet.Range("BCY51:BCZ60") ' topics
            .Range("G" & (holomemIndex - 2) * 23 + 11 & ":G" & (holomemIndex - 2) * 23 + 20).Copy ActiveSheet.Range("BDC51:BDC60") ' topics
        End With
        
        ' get colors
        noStreamColor = Worksheets("colors").Cells(holomemIndex, 2).Value
        oneStreamColor = Worksheets("colors").Cells(holomemIndex, 3).Value
        mostStreamedColor = Worksheets("colors").Cells(holomemIndex, 4).Value

        ' conditional formatting
        For rowNum = 4 To 10
            Set rg = ActiveSheet.Range("B" & rowNum & ":BCK" & rowNum)
            Set cs = rg.FormatConditions.AddColorScale(ColorScaleType:=3)
           
            With cs
                With .ColorScaleCriteria(1)
                     .FormatColor.color = HexToRgbLong(noStreamColor)
                     .Type = xlConditionValueNumber
                     .Value = 0
                End With
                With .ColorScaleCriteria(2)
                     .FormatColor.color = HexToRgbLong(oneStreamColor)
                     .Type = xlConditionValueFormula
                     ' smallest value except 0
                     .Value = "=MIN(IF($B$" & rowNum & ":$BCK$" & rowNum & ">0,$B$" & rowNum & ":$BCK$" & rowNum & "))"
                End With
                With .ColorScaleCriteria(3)
                     .FormatColor.color = HexToRgbLong(mostStreamedColor)
                     .Type = xlConditionValueHighestValue
                End With
            End With
        Next rowNum

        With ActiveSheet
            ' channel name
            .Range("B2:BCK2").Formula = "=" & indexFormula(holomemName, "ch_name")
            ' apply bottom border
            .Range("B3:BCK3").Borders(xlEdgeBottom).Weight = xlThin
            ' stats
            .Range("BCP14").Formula = "=""Livestreams: "" & " & indexFormula(holomemName, "count")
            .Range("BCP15").Formula = "=""Total length in hours (D:HH:MM): "" & " & "TEXT(" & "" & indexFormula(holomemName, "total_hrs") & "" & ", ""#,###"")" & " & "" (""" & " & " & "" & indexFormula(holomemName, "total_f") & "" & " & "")"""
            .Range("BCP16").Formula = "=""Average length/stream in minutes (H:MM): "" & " & "TEXT(" & "" & indexFormula(holomemName, "avg_mins") & "" & ", ""#,###"")" & " & "" (""" & " & " & "" & indexFormula(holomemName, "avg_f") & "" & " & "")"""
            .Range("BCP17:BDG17").Formula = "=""Most streamed times (day (time-range/s) amount): "" & " & indexFormula(holomemName, "most_overlap")
            .Range("BCW51").Formula = "=" & indexFormula(holomemName, "count") & " - " & indexFormula(holomemName, "missing")
            .Range("BCW52").Formula = "=" & indexFormula(holomemName, "missing")
        End With

        ' color charts
        For Each co In ActiveSheet.ChartObjects
            co.Activate
            ActiveChart.SeriesCollection(1).Interior.color = HexToRgbLong(mostStreamedColor)
        Next co
        ' color pie chart slice to a different color
        ActiveSheet.ChartObjects(3).Activate
        ActiveChart.SeriesCollection(1).Points(2).Interior.color = HexToRgbLong(noStreamColor)
        ' color double bar chart
        ActiveSheet.ChartObjects(4).Activate
        ActiveChart.Legend.LegendEntries(1).LegendKey.Interior.Color = HexToRgbLong(mostStreamedColor)
        ActiveChart.Legend.LegendEntries(2).LegendKey.Interior.Color = HexToRgbLong(oneStreamColor)
    Next holomemIndex
End Sub