if [ !$(lsusb | grep HackRF | wc -l) ]
then
echo "Found HackRF"
fi

# Now we check the internet and install the necessary components
python get-pip.py
sudo apt install git-all


