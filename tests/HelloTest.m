classdef HelloTest < matlab.unittest.TestCase
    methods (Test)
        function testHelloReturnsCorrectMessage(testCase)
            message = hello();
            testCase.verifyEqual(message, "hello world");
        end

        function testHelloOutputIsString(testCase)
            message = hello();
            testCase.verifyClass(message, 'string');
        end
    end
end
