//-----------------------------------------------------------------------
// Copyright 2019 Damien Pretet
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//-----------------------------------------------------------------------

`timescale 1 ns / 1 ps
`default_nettype none

module Adder

    #(
    parameter WIDTH = 8
    )(
    input  wire            aclk,
    input  wire            arstn,
    input  wire            clr,
    input  wire            inc,
    output reg [WIDTH-1:0] out
    );

    always @ (posedge aclk or negedge arstn) begin

        if (arstn == 1'b0) begin
            out <= {WIDTH{1'b0}};
        end
        else begin
            if (clr == 1'b1)
                out <= 8'b0;
            else if (inc == 1'b1)
                out <= out + 1'b1;
        end
    end

endmodule

`resetall

