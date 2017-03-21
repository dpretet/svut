//-----------------------------------------------------------------------------
// Copyright Damien Pretet ThotIP
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
//-----------------------------------------------------------------------------  

`timescale 1 ns / 1 ps
`default_nettype none

module adder

    #(
    parameter LATENCY = 0,  
    parameter WIDTH = 32
    )(
    input  wire             aclk,
    input  wire             arstn,
    input  wire             srst,
    input  wire [WIDTH-1:0] a,
    input  wire [WIDTH-1:0] b,
    output wire [WIDTH-1:0] c
    );

    generate begin

        if (LATENCY == 0) begin
            assign c = a + b;
        end
        else begin
            
            reg [WIDTH-1:0] c_reg;

            always @ (posedge aclk or negedge arstn) begin

                if (arstn == 1'b0) begin
                    c_reg <= {WIDTH{1'b0}};
                end
                else if (srst == 1'b1) begin
                    c_reg <= {WIDTH{1'b0}};
                end
                else begin
                    c_reg <= a + b;
                end
            end
            
            assign c = c_reg;

        end

    end
    endgenerate

endmodule

`resetall

