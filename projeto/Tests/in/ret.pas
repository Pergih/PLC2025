program TestArrayReturn;

var
    myArray : array [1..3] of integer;

function SumArray : integer;
var
    i, total : integer;
begin
    total := 0;
    for i := 1 to 3 do
        total := total + myArray[i];
    SumArray := total;
end;

begin
    myArray[1] := 10;
    myArray[2] := 20;
    myArray[3] := 30;

    writeln('Soma do array: ', SumArray());
end.
