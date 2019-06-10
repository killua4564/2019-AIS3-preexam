### Are you admin?
```
#!/usr/bin/ruby
require 'json'

STDOUT.sync = true
puts "Your name:"
name = STDIN.gets.chomp
puts "Your age:"
age = STDIN.gets.chomp
if age.match(/[[:alpha:]]/)
    puts "No!No!No!"
    exit
end

string = "{\"name\":\"#{name}\",\"is_admin\":\"no\", \"age\":\"#{age}\"}"
res = JSON.parse(string)
if res['is_admin'] == "yes"
    puts "AIS3{xxxxxxxxxxxx}"  # flag is here
else
    puts "Hello, " + res['name']
    puts "You are not admin :("
end
```
- 第一點要先用json的特性去把原本server上的is_admin繞過 padding成自己的
- 第二點ruby的`age.match(/[[:alpha:]]/)`並沒有過濾`{`,`"`等特殊字元
- payload:
    - name: `asd","is_admin":"yes","":{"":"`
    - age: `"},"":"1`
    - json結果: `{"name":"asd","is_admin":"yes","":{"":"", "is_admin":"no","age":""},"":"1"}`