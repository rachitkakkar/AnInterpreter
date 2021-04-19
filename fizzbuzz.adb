let num = 0;

if num < 100 {
    reassign num = num + 1;
    print_expr_ln num;
    jump 10;
    jump 3;
}
jump 23;
if num%15 == 0 {
    print_str_ln FIZZBUZZ;
    jump 3;
}
if num%3 == 0 {
    print_str_ln FIZZ;
    jump 3;
}
if num%5 == 0 {
    print_str_ln BUZZ;
    jump 3;
}
jump 3;
print_str_ln DONE;