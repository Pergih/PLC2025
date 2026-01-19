program ComplexTest;

var
    i, j, total : integer;
    x : integer;

function DoubleValue(a : integer) : integer;
begin
    DoubleValue := a * 2;
end;

begin
    total := 0;

    writeln('Contagem crescente com if/else:');
    for i := 1 to 5 do
    begin
        if i mod 2 = 0 then
            writeln('Par: ', i)
        else
            writeln('Impar: ', i);

        total := total + DoubleValue(i);
    end;

    writeln('Total acumulado: ', total);

    writeln('Contagem decrescente usando downto:');
    for j := 5 downto 1 do
    begin
        x := DoubleValue(j);
        writeln('j=', j, ', x=', x);
    end;
end.
