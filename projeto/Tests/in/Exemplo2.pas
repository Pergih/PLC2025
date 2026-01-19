program FibArrayExample;

var
    n, i: integer;
    fibArr: array [1..20] of integer;

function Fib(k: integer): integer;
begin
    if k <= 2 then
        Fib := 1
    else
        Fib := fibArr[k - 1] + fibArr[k - 2];
end;


begin
    n := 10;
    fibArr[1] := 1;
    fibArr[2] := 1;

    for i := 3 to n do
    begin
        fibArr[i] := Fib(i);
    end;

    for i := 1 to n do
        writeln(fibArr[i]);
end.
