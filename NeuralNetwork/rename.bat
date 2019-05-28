@echo off
setlocal enableDelayedExpansion
set i=1
for %%F in (WIN*) do (
	set "name=%%F"
	ren "!name!" "F!i!.jpg"
	set /A i=i+1
)