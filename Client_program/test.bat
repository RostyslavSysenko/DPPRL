
for /l %%x in (0, 20, 40) do (
	for /l %%y in (20,30,110) do (
		for /l %%z in (1, 1, 18) do (
			python -u ClientEncoder.py 3 5 %%x %%y
			echo %%x
			echo %%y
		)
	)

)


PAUSE