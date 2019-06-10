### Trivial
- 用ida開 觀察到sub_76A的部分應該就是會把flag算出來然後跟你的input做比對
- 是也可以寫個script去把它比對的flag自己算出來 但是我想說他當下才算 所以應該會在stack裡吧
- 停在0x0x555555554e01的位置 然後sub_76A一開始說需要長度大於0x32的字串 所以run起來後輸入"A" * 0x33 之後就可以在stack上看到flag了
```
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe850 --> 0x0 
0008| 0x7fffffffe858 --> 0x7fffffffe870 ("AIS3{This_is_a_rea", 'l' <repeats 11 times>, "y_boariiing_challenge}")
0016| 0x7fffffffe860 --> 0x7fffffffe8c0 --> 0x555555554e80 (push   r15)
0024| 0x7fffffffe868 --> 0x555555554e43 (test   eax,eax)
0032| 0x7fffffffe870 ("AIS3{This_is_a_rea", 'l' <repeats 11 times>, "y_boariiing_challenge}")
0040| 0x7fffffffe878 ("s_is_a_rea", 'l' <repeats 11 times>, "y_boariiing_challenge}")
0048| 0x7fffffffe880 ("ea", 'l' <repeats 11 times>, "y_boariiing_challenge}")
0056| 0x7fffffffe888 ("llllly_boariiing_challenge}")
```
- flag: `AIS3{This_is_a_reallllllllllly_boariiing_challenge}`