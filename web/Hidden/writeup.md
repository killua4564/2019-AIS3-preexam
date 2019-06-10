### Hidden
- 題目給了一個很亂的`hidden.js`
- prettify後發現裡面有個`flag.js`在compile的時候import進來了
- 然後被代換成`nHHx`的key 沿路找上去發現個包起來好幾層的lambda func
- 複製下來丟入console然後輸入他說要的數字 flag就print出來了