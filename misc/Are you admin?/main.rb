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

puts string

res = JSON.parse(string)

puts res

if res['is_admin'] == "yes"
    puts "AIS3{xxxxxxxxxxxx}"  # flag is here
else
    puts "Hello, " + res['name']
    puts "You are not admin :("
end
