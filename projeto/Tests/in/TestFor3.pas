program TestFor3;

var
    i : integer;
    s : integer;

begin
    s := 0;

    for i := 1 to 10 do
    begin
        s := s + i;
        writeln(s);
    end;
end.