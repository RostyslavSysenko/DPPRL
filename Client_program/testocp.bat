

for /l %%y in (20,30,110) do (
	for /l %%z in (1, 1, 18) do (
		python -u ClientEncoder.py 3 5 20 %%y
		echo %%y
		echo %%z
	)
)
PAUSE