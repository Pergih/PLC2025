program TestForFunc;

var
    i : integer;

function SumTo(n : integer) : integer;
var
    total, j : integer;
begin
    total := 0;
    for j := 1 to n do
        total := total + j;
    SumTo := total;
end;

begin
    writeln(SumTo(5));
end.
