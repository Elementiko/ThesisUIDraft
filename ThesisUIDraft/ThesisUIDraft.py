import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import flet as ft
import pandas as pd
import csv
from csv import writer
import random
from flet import *
from flet import ControlEvent
from flet_timer.flet_timer import Timer
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads1 = ADS.ADS1115(i2c,address=0x48)
ads2 = ADS.ADS1115(i2c,address=0x49)

chan = AnalogIn(ads1, ADS.P0)
chan1 = AnalogIn(ads1, ADS.P1)
chan2 = AnalogIn(ads1, ADS.P2)
chan3 = AnalogIn(ads1, ADS.P3)
chan4 = AnalogIn(ads2, ADS.P0)
chan5 = AnalogIn(ads2, ADS.P1)
chan6 = AnalogIn(ads2, ADS.P2)
chan7 = AnalogIn(ads2, ADS.P3)



MQ2 = chan.value
MQ3 = chan1.value
MQ4 = chan2.value
MQ5 = chan3.value
MQ6 = chan4.value
MQ7 = chan5.value
MQ8 = chan6.value
MQ135 = chan7.value


Normal = pd.read_csv('objects/normal.csv')



def main(page: ft.Page) -> None:
    page.title = 'Increment Counter'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = 'light'
    page.window.full_screen = True

    SnapshotValues = ["","","","","","",'"',"",""]

    Prev1 = ['0','0','0','0','0','0','0','0']
    Prev2 = ['0','0','0','0','0','0','0','0']

    text_number: TextField = TextField(value = '0', text_align= ft.TextAlign.RIGHT, width = 100)

    MQ2Display: TextField = TextField(value = str(MQ2), text_align = ft.TextAlign.CENTER, width = 100)
    MQ3Display: TextField = TextField(value = str(MQ3), text_align = ft.TextAlign.CENTER, width = 100)
    MQ4Display: TextField = TextField(value = str(MQ4), text_align = ft.TextAlign.CENTER, width = 100)
    MQ5Display: TextField = TextField(value = str(MQ5), text_align = ft.TextAlign.CENTER, width = 100)
    MQ6Display: TextField = TextField(value = str(MQ6), text_align = ft.TextAlign.CENTER, width = 100)
    MQ7Display: TextField = TextField(value = str(MQ7), text_align = ft.TextAlign.CENTER, width = 100)
    MQ8Display: TextField = TextField(value = str(MQ8), text_align = ft.TextAlign.CENTER, width = 100)
    MQ135Display: TextField = TextField(value = str(MQ135), text_align = ft.TextAlign.CENTER, width = 100)

    def OpenSetNormal(e: ControlEvent) -> None:
        
        NSV = [MQ2Display.value,
               MQ3Display.value,
               MQ4Display.value,
               MQ5Display.value,
               MQ6Display.value,
               MQ7Display.value,
               MQ8Display.value,
               MQ135Display.value]

        def SetNewNomral(e):
            Normal.loc[0, 'MQ2'] = NSV[0]
            Normal.loc[0, 'MQ3'] = NSV[1]
            Normal.loc[0, 'MQ4'] = NSV[2]
            Normal.loc[0, 'MQ5'] = NSV[3]
            Normal.loc[0, 'MQ6'] = NSV[4]
            Normal.loc[0, 'MQ7'] = NSV[5]
            Normal.loc[0, 'MQ8'] = NSV[6]
            Normal.loc[0, 'MQ135'] = NSV[7]
            Normal.to_csv('objects/normal.csv')
            page.close(SetNormalPrompt)

        # Create a new instance of the dialog
        SetNormalPrompt = ft.AlertDialog(
                title=ft.Text("Set Normal Values"),
                content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("MQ2")),
                    ft.DataColumn(ft.Text("MQ3")),
                    ft.DataColumn(ft.Text("MQ4")),
                    ft.DataColumn(ft.Text("MQ5")),
                    ft.DataColumn(ft.Text("MQ6")),
                    ft.DataColumn(ft.Text("MQ7")),
                    ft.DataColumn(ft.Text("MQ8")),
                    ft.DataColumn(ft.Text("MQ135")),
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(NSV[0])),
                        ft.DataCell(ft.Text(NSV[1])),
                        ft.DataCell(ft.Text(NSV[2])),
                        ft.DataCell(ft.Text(NSV[3])),
                        ft.DataCell(ft.Text(NSV[4])),
                        ft.DataCell(ft.Text(NSV[5])),
                        ft.DataCell(ft.Text(NSV[6])),
                        ft.DataCell(ft.Text(NSV[7])),
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(Normal['MQ2'][0])),
                        ft.DataCell(ft.Text(Normal['MQ3'][0])),
                        ft.DataCell(ft.Text(Normal['MQ4'][0])),
                        ft.DataCell(ft.Text(Normal['MQ5'][0])),
                        ft.DataCell(ft.Text(Normal['MQ6'][0])),
                        ft.DataCell(ft.Text(Normal['MQ7'][0])),
                        ft.DataCell(ft.Text(Normal['MQ8'][0])),
                        ft.DataCell(ft.Text(Normal['MQ135'][0])),
                    ]),
                ],
                width=1000,
            ),
            actions=[
                ft.TextButton("Confirm", on_click=SetNewNomral),
                ft.TextButton("Cancel", on_click=lambda e: page.close(SetNormalPrompt), style=ButtonStyle(color='red')),
            ],
        )

        # Open the dialog
        page.open(SetNormalPrompt)

    def OpenViewSamples(e: ControlEvent) -> None:
        def RemoveSample(e):
            RSD = pd.read_csv('objects/dataset.csv')
            RSD = RSD.drop(e.control.data).reset_index(drop=True)
            RSD.to_csv('objects/dataset.csv',index=False)
            page.close(ViewSamplePrompt)
        
        SampleSize = 0
        df = pd.read_csv('objects/dataset.csv')
        SampleList = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("MQ2")),
                    ft.DataColumn(ft.Text("MQ3")),
                    ft.DataColumn(ft.Text("MQ4")),
                    ft.DataColumn(ft.Text("MQ5")),
                    ft.DataColumn(ft.Text("MQ6")),
                    ft.DataColumn(ft.Text("MQ7")),
                    ft.DataColumn(ft.Text("MQ8")),
                    ft.DataColumn(ft.Text("MQ135")),
                    ft.DataColumn(ft.Text("Label")),
                    ft.DataColumn(ft.Text("")),
                ],
                rows=[],
                width=1000,
            )

        for item in df.index:
               SampleList.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(df['MQ2'][item])),
                                                              ft.DataCell(ft.Text(df['MQ3'][item])),
                                                              ft.DataCell(ft.Text(df['MQ4'][item])),
                                                              ft.DataCell(ft.Text(df['MQ5'][item])),
                                                              ft.DataCell(ft.Text(df['MQ6'][item])),
                                                              ft.DataCell(ft.Text(df['MQ7'][item])),
                                                              ft.DataCell(ft.Text(df['MQ8'][item])),
                                                              ft.DataCell(ft.Text(df['MQ135'][item])),
                                                              ft.DataCell(ft.Text(df['Label'][item])),
                                                              ft.DataCell(ft.ElevatedButton("Remove Sample",data = item, on_click = RemoveSample))]))
               SampleSize += 1

        # Create a new instance of the dialog
        ViewSamplePrompt = ft.AlertDialog(
                title=ft.Text("Sample Set"),
                content= ft.Column(controls=[SampleList],scroll=ScrollMode.AUTO,height=100),
            actions=[
                ft.Text("Sample Size: " + str(SampleSize)),
                ft.TextButton("Cancel", on_click=lambda e: page.close(ViewSamplePrompt), style=ButtonStyle(color='red')),
            ],
        )

        # Open the dialog
        page.open(ViewSamplePrompt)

    def OpenAddSample(e:ControlEvent) -> None:
        
        def AddSample(e) -> None:
           SnapshotValues[8] = SampleLabel.value
           with open ('objects/dataset.csv','a',newline='') as AppendCatalog:
            writerCatalog = writer(AppendCatalog)
            writerCatalog.writerow(SnapshotValues)
            AppendCatalog.close()
           e.page.close(AddSamplePrompt)

        SampleLabel = ft.Dropdown(
            width=100,
            options=[
                ft.dropdown.Option("Bangus"),
                ft.dropdown.Option("Galunggong"),
                ft.dropdown.Option("Lapu-lapu"),
                ft.dropdown.Option("Tilapia"),
                    ])

        SnapshotValues[0] = MQ2Display.value
        SnapshotValues[1] = MQ3Display.value
        SnapshotValues[2] = MQ4Display.value
        SnapshotValues[3] = MQ5Display.value
        SnapshotValues[4] = MQ6Display.value
        SnapshotValues[5] = MQ7Display.value
        SnapshotValues[6] = MQ8Display.value
        SnapshotValues[7] = MQ135Display.value
        AddSamplePrompt = AlertDialog(title=ft.Text("Add Sample"),
                                  content= ft.DataTable(
                                                       columns=[
                                                        ft.DataColumn(ft.Text("MQ2")),
                                                        ft.DataColumn(ft.Text("MQ3")),
                                                        ft.DataColumn(ft.Text("MQ4")),
                                                        ft.DataColumn(ft.Text("MQ5")),
                                                        ft.DataColumn(ft.Text("MQ6")),
                                                        ft.DataColumn(ft.Text("MQ7")),
                                                        ft.DataColumn(ft.Text("MQ8")),
                                                        ft.DataColumn(ft.Text("MQ135"))],
                                                       rows = [ft.DataRow(cells = [
                                                        ft.DataCell(ft.Text(SnapshotValues[0])),
                                                        ft.DataCell(ft.Text(SnapshotValues[1])),
                                                        ft.DataCell(ft.Text(SnapshotValues[2])),
                                                        ft.DataCell(ft.Text(SnapshotValues[3])),
                                                        ft.DataCell(ft.Text(SnapshotValues[4])),
                                                        ft.DataCell(ft.Text(SnapshotValues[5])),
                                                        ft.DataCell(ft.Text(SnapshotValues[6])),
                                                        ft.DataCell(ft.Text(SnapshotValues[7]))])],
                                                       width=1000),
                                  actions=[SampleLabel,
                                           ft.TextButton("Confirm",on_click= AddSample),
                                           ft.TextButton("Cancel",on_click= lambda e: page.close(AddSamplePrompt),style=ButtonStyle(color='red'))])
        e.page.open(AddSamplePrompt)



    
    def refresh() -> None:
        
        NSV = [MQ2Display.value,
               MQ3Display.value,
               MQ4Display.value,
               MQ5Display.value,
               MQ6Display.value,
               MQ7Display.value,
               MQ8Display.value,
               MQ135Display.value]

        for i in range(8):
               Prev2[i] = Prev1[i]
               Prev1[i] = NSV[i]
        
        
        MQ2Display.value = str(chan.value)
        MQ3Display.value = str(chan1.value)
        MQ4Display.value = str(chan2.value)
        MQ5Display.value = str(chan3.value)
        MQ6Display.value = str(chan4.value)
        MQ7Display.value = str(chan5.value)
        MQ8Display.value = str(chan6.value)
        MQ135Display.value = str(chan7.value)

        HoldMQ = [MQ2Display.value,MQ3Display.value,MQ4Display.value,MQ5Display.value,MQ6Display.value,MQ7Display.value,MQ8Display.value,MQ135Display.value]
        MQName = ['MQ2','MQ3','MQ4','MQ5','MQ6','MQ7','MQ8','MQ135']

        for i in range(8):
            if abs(int(HoldMQ[i]) - int(Normal[MQName[i]][0])) <= 1:
                HoldMQ[i] = 'green'
            else:
                if abs(int(HoldMQ[i]) - int(Prev1[i])) <= 1 and \
                abs(int(HoldMQ[i]) - int(Prev2[i])) <= 1 and \
                abs(int(Prev1[i]) - int(Prev2[i])) <= 1:
                    HoldMQ[i] = 'blue'
                else:
                    HoldMQ[i] = 'black'

        MQ2Display.color = HoldMQ[0]
        MQ3Display.color = HoldMQ[1]
        MQ4Display.color = HoldMQ[2]
        MQ5Display.color = HoldMQ[3]
        MQ6Display.color = HoldMQ[4]
        MQ7Display.color = HoldMQ[5]
        MQ8Display.color = HoldMQ[6]
        MQ135Display.color = HoldMQ[7]

        page.update()
        
    timer = Timer(name="timer",interval_s=1,callback=refresh)
    SetNormalButton: ElevatedButton = ElevatedButton(text ='Set Normal',on_click=OpenSetNormal)
    AddSampleButton: ElevatedButton = ElevatedButton(text = 'Add Sample',on_click=OpenAddSample)
    ViewDataButton : ElevatedButton = ElevatedButton(text = 'View Dataset',on_click=OpenViewSamples)

    C1: Column = Column(controls=[ft.Text("MQ2",size=20,weight=ft.FontWeight.BOLD),MQ2Display,ft.Text("MQ6",size=20,weight=ft.FontWeight.BOLD),MQ6Display])
    C2: Column = Column(controls=[ft.Text("MQ3",size=20,weight=ft.FontWeight.BOLD),MQ3Display,ft.Text("MQ7",size=20,weight=ft.FontWeight.BOLD),MQ7Display])
    C3: Column = Column(controls=[ft.Text("MQ4",size=20,weight=ft.FontWeight.BOLD),MQ4Display,ft.Text("MQ8",size=20,weight=ft.FontWeight.BOLD),MQ8Display])
    C4: Column = Column(controls=[ft.Text("MQ5",size=20,weight=ft.FontWeight.BOLD),MQ5Display,ft.Text("MQ135",size=20,weight=ft.FontWeight.BOLD),MQ135Display])
    C5: Column = Column(controls=[SetNormalButton,AddSampleButton,ViewDataButton])

    page.add(timer,
        ft.Row(
            [C1,C2,C3,C4,C5],
            alignment = ft.MainAxisAlignment.CENTER)
        
    )

if __name__ == '__main__':
    ft.app(target=main)

