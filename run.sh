if [[ $1 == "" ]]; then
	echo "Usage: run.sh HH:MM"
	exit 1
fi
echo "python main.py" | at $1
