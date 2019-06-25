Visualize
===

### Requirements

- python3
- tkinter

## Usage:


## [canvas.py](https://github.com/raywu0123/Algorithms-2019Spring-Final-Project/blob/master/visualize/canvas.py)

1. `python3 canvas.py [write_file_name]`

會跳出一個空白視窗

2. 接著按"m"，開始畫M1的polygons

- 在想要的位置用滑鼠點，畫polygon，可以畫不止一個

- 如果剩兩條線可以連回起點，按"e"可以自動連線

- 如果有三個點在同一條線上面的狀況，等等他會自己去掉

3. 畫好了接著按"c"開始畫C1的polygons，可以畫不止一個
4. 重複2. 3. 直到畫完直接關掉視窗，檔案就會寫入了

![](https://i.imgur.com/fTUwZgU.jpg)

## [draw_tk.py](https://github.com/raywu0123/Algorithms-2019Spring-Final-Project/blob/master/visualize/draw_tk.py)


1. `python3 draw_tk.py sample.in sample.out [window size(建議1000)]`
2. 一直按"r"，一開始會把Merge跟Clip依序加入圖中，Merge是紅色Clip是綠色，M跟C都加完，會開始疊sample.out裡面最後split完的rectangles，要提前結束的話按"e"。
