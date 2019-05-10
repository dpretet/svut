`timescale 1 ns / 1 ps

module ffd

    (
    input  wire aclk,
    input  wire arstn,
    input  wire d,
    output reg  q
    );

    always @ (posedge aclk or negedge arstn) begin
        if (arstn == 1'b0) q <= 1'b0;
        else q <= d;
    end

endmodule
