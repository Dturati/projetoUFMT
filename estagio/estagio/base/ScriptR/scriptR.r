grafico = function()
{
    # Define the cars vector with 5 values
    cars <- c(1, 3, 6, 4, 7)

    # Graph cars using blue points overlayed by a line
    plot(cars, type="o", col="blue")

    # Create a title with a red, bold/italic font
    title(main="", col.main="red", font.main=4)
    dev.copy(jpeg,filename="plot.jpg");
        dev.off ();
}

grafico()