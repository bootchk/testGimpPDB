# generateRemoved.sh

comm -23 namesInEarlyVersion namesInLateVersion > namesRemovedOrDeprecated
comm -23 namesRemoved allDeprecated > removed
