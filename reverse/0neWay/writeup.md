### 0neWay
- binary 要你輸入一堆東西 然後hash對了才會利用這些input去xor出flag.jpg
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  puts("-----");
  puts("I encrypted a image in this binary,");
  puts("you have to answer my questions to decrypt it,");
  puts("cuz only my friends can view this secret image");
  puts("-----");
  puts("Who am I? (lowercase)");
  __isoc99_scanf("%4s", s);
  v9 = strlen(s);
  puts("How old am I?");
  __isoc99_scanf("%2s", &s[v9]);
  v9 = strlen(s);
  puts("What the name of my first pet? (lowercase)");
  __isoc99_scanf("%20s", &s[v9]);
  v9 = strlen(s);
  v3 = hash(&v9);
  v4 = v9;
  v5 = hash(s);
  printf("%s, %lu, %d, %lu", s, v5, v4, v3);
  if ( hash(&v9) == 177593 && hash(s) == 8932587927620123215LL )
  {
    ptr = &binary_flag_jpg_start;
    v10 = 0;
    stream = fopen("./flaggggg.jpg", "w");
    if ( stream )
    {
      while ( ptr != &binary_flag_jpg_end )
      {
        v7 = v10++;
        *(_BYTE *)ptr ^= s[v7 % v9];
        v8 = ptr;
        ptr = (char *)ptr + 1;
        fwrite(v8, 1uLL, 1uLL, stream);
      }
      puts("you got my secret photo");
      fclose(stream);
      result = 0;
    }
    else
    {
      puts("write file error !");
      result = -2;
    }
  }
  else
  {
    puts("haker haker go away");
    result = -1;
  }
  return result;
}
```
- 注意到`&binary_flag_jpg_start`和`&binary_flag_jpg_end`
- 構造idc payload把data存成jpg看看
```
import idc

ea = 0x202010  #binary_flag_jpg_start
ea_stop = 0x22ec59  #binary_flag_jpg_end

with open("flag.jpg", "wb") as flag:
	while ea <= ea_stop:
		flag.write(chr(idc.Byte(ea)))
		ea += 1
```
- 果然出來一個壞檔 很明顯是xor過的 所以...
- `$ xortool flag.jpg -l 20 -c 20`
- 長度部分可以用`hash(&v9) == 177593`這個部分反推
- flag: ![](flag.out.jpg)
