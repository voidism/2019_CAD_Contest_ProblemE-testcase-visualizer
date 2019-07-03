2019 CAD Contest ProblemE testcase & visualizer
===

### Requirements

- python3
- tkinter

## Usage:


## Generate manual test case 

1. 
```
python3 canvas.py [write_file_name]
```

會跳出一個空白視窗

2. 接著按"m"，開始畫M1的polygons

- 在想要的位置用滑鼠點，畫polygon，可以畫不止一個

- 如果剩兩條線可以連回起點，按"e"可以自動連線

- 如果有三個點在同一條線上面的狀況，等等他會自己去掉

3. 畫好了接著按"c"開始畫C1的polygons，可以畫不止一個
4. 重複2. 3. 直到畫完直接關掉視窗，檔案就會寫入了

![](https://i.imgur.com/fTUwZgU.jpg)

## Visualize input/output file pairs

1. 
```
python3 draw_tk.py sample.in sample.out [window size(建議1000)]
```

2. 一直按"r"，一開始會把Merge跟Clip依序加入圖中，Merge是紅色Clip是綠色，M跟C都加完，會開始疊sample.out裡面最後split完的rectangles，要提前結束的話按"e"。

## Random generate test case

- rectangle test case only
- Merge Clip 交替
- 如果想讓測資的長寬範圍大一點，可以調[第90行](https://github.com/voidism/2019_CAD_Contest_ProblemE-testcase-visualizer/blob/3b90131e1d41a66d8a7f4b2895b3414ff6de360c/random_case.py#L90)這邊的height跟width，目前只有設1000/600。

```
python random_case.py [output_file_name] [# of pairs of Merge and Clip] [# of rectangles in a Merge or Clip]
```

## Verify by boolean mask

- don't use this program to verify files that are over size (e.g. over 1000000 in window size), it will need large memory.

```
python verify.py [input_file_name] [output_file_name] [window size of testcase (max width of height)]
```

## Random testing

- `./myPolygon` is needed in the same directory.
- it will save the error case automatically for you to debug!
- the error case and error output will be named as `errorcase.in.*`, `errorcase.out.*`.

```
bash run_test.sh [# of random testcase] [# of pairs of Merge and Clip in each testcase] [# of rectangles in a Merge or Clip]
```

---
2019 CAD Contest Link: http://iccad-contest.org/2019/tw/problems.html
