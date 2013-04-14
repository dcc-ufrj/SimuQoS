#rm -rf ../resultado/aleatory/*
#rm -rf ../resultado/sequential/*
for i in 1 2 3 4 5 6 7 8 9 10
do
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 10 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 10 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 10 120 sequential 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 10 120 sequential 30 0;

python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 30 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 30 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 30 120 sequential 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 30 120 sequential 30 0;

python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 50 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 50 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 50 120 sequential 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 50 120 sequential 30 0;

python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 70 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 70 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 70 120 sequential 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 70 120 sequential 30 0;

python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 100 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 100 120 aleatory 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 sequential 100 120 sequential 30 0;
python ../classes/Main.py 50 120 120 5000 unitario aleatorio 1 aleatory 100 120 sequential 30 0;
echo $i;
done
python ../classes/Main.py
