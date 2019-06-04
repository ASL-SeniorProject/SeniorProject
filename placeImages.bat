@echo off
setlocal enableDelayedExpansion
set i=1
for %%F in (*.jpg) do (
	set name=%%F
	set ext=!name:~0,1!
	set loc=NeuralNetwork\BlueHandAlphabet\Images\!ext!
	move !name! !loc!
)