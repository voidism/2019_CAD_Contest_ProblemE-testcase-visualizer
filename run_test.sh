err_file_num=0

for entry in ./* ; do
    if [[ $entry =~ ^\./errorcase\.in.* ]]; then
        ((err_file_num++))
    fi
done
echo "existed errorcase file: $err_file_num"

#cd ../build/ && cmake ../src && make && cd ../visualize

for ((i=1; i<=$1; i++)); do
    python random_case.py random.in.$i $2 $3
    ./myPolygon  random.in.$i random.out.$i > /dev/null
    python verify.py random.in.$i random.out.$i 1000
    if [ "$?" -ne 0 ]; then
        echo "error occurs in random.in.$i. restart with SV."
        sed -i 's/SO/SV/g' random.in.$i
        ./myPolygon  random.in.$i random.out.$i > /dev/null
        python verify.py random.in.$i random.out.$i 1000
        if [ "$?" -ne 0 ]; then
            echo "error occurs in random.in.$i. restart with SH"
            sed -i 's/SV/SH/g' random.in.$i
            ./myPolygon  random.in.$i random.out.$i > /dev/null
            python verify.py random.in.$i random.out.$i 1000
            if [ "$?" -ne 0 ]; then
                echo "error still occurs in random.in.$i. Abort!"
                sed -i 's/SH/SO/g' random.in.$i
            else 
                echo "pass with SH!"
                sed -i 's/SH/SO/g' random.in.$i
            fi
        else
            echo "pass with SV!"
            sed -i 's/SV/SO/g' random.in.$i
        fi
        ((err_file_num++))
        cp random.in.$i errorcase.in.$err_file_num
        cp random.out.$i errorcase.out.$err_file_num
        rm random.in.$i random.out.$i
        break
    fi
    rm random.in.$i random.out.$i
    # read -p "Press enter to continue"
done;
