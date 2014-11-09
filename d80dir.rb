#!/usr/bin/env ruby
require 'tempfile'

filename = ARGV[0]
abort "Usage d80dir <filename>" unless filename && File.exist?(filename)

# if the image has error info at the end, c1541 can't read it,
# so create a tempfile without the error info
tempfile = nil
if filename.end_with?(".d80") && File.size(filename) > 533248
  tempfile = Tempfile.new(["d80dir", ".d80"])
  data = IO.binread(filename, 533248)
  IO.binwrite(tempfile.path, data)
  filename = tempfile.path
end

# scrape output from c1541
out = IO.popen("c1541 '#{filename}'", "r+") do |pipe|
  pipe.puts "dir"
  pipe.close_write
  pipe.read
end
lines = out.split("\n")

# remove version/copyright info
i = lines.index {|line| line.start_with?("c1541 #8> ")}
lines = lines.slice(i, lines.size)

# remove prompts and empty lines
lines.map! { |line| line.sub /^c1541 #8> /, '' }
lines.reject! { |line| line.strip.size.zero? }

# print the directory
lines.each { |line| puts line }

# unlink tempfile if we made one
tempfile.unlink if tempfile
