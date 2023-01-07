
def arrange_stock(file=r"compare_results\stock_out.txt"):
    output = []
    with open(file, "r") as f:
        for line in f.readlines():
            output.append(line.strip())
    
    return output

def main():
    with open(r"compare_results\my_out.txt", "r") as my_out:
        output1 = []
        output2 = arrange_stock()

        for line in my_out.readlines():
            output1.append(line.strip())


        for line in output1:
            for line2 in output2:
                l1_move, l1_num = line.split(" ")
                l2_move, l2_num = line2.split(" ")
                if l1_move ==  l2_move:
                    if int(l1_num) != int(l2_num):
                        print("My output    ", line)
                        print("Stock output ", line2)
                        print("-----")


    
main()