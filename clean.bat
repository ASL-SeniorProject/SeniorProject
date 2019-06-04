@echo off
setlocal enableDelayedExpansion
set i=1
for %%F in (*.jpg) do (
	del %%F
)