
def arrange_stock(file=r"compare_results\stock_out.txt"):
    output = []
    with open(file, "r") as f:
        for line in f.readlines():
            temp = line.replace(":", "")
            temp = list(temp)
            temp.insert(2, " ")
            temp = "".join(temp).strip()
            output.append(temp)
    
    return output

def main():
    with open(r"compare_results\my_out.txt", "r") as my_out:
        output1 = []
        output2 = arrange_stock()

        for line in my_out.readlines():
            output1.append(line.strip())


        for line in output1:
            for line2 in output2:
                if line[:5] ==  line2[:5]:
                    if int(line[-2:]) != int(line2[-2:]):
                        print("My output ", line)
                        print("Stock output ", line2)

    

main()