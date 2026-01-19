program TestRepeat;

var
    i : integer;
begin
    i := 0;
    repeat
        writeln(i);
        i := i+1;
    until i = 5;
end.
