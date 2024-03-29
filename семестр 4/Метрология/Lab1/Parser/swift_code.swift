func functionName1(parameter1: Type1, parameter2: Type2, parameter3: Type1) -> ReturnType1 {
    let x = 42
		var y = x + 10
		if y > 0 {
		    print("Positive")
		} else if x < 0 {
		    print("Negative")
		} else {
		    print("Zero")
		}
}

func functionName2(_ parameter: Type) -> ReturnType2 {
    switch value {
        case 1:
            print("Case 1")
        case 2:
            print("Case 2")
        default:
            print("Default Case")
        }

    switch anotherValue {
        case "A":
            print("Case A")
        case "B":
            print("Case B")
        }
    }

func functionName3() -> ReturnType3 {
    # function body
}

func outerFunction() -> ReturnType3 {
    let outerVariable = 10

    for item in array {
		    print(item)
		}

		for number in 1...5 {
		    print(number)
		}

    switch value {
        case 1:
            print("Case 1")
        case 2:
            print("Case 2")
        default:
            print("Default Case")
        }

    func innerFunction() {
        print("Inside innerFunction, outerVariable is")
    }

    innerFunction()
    let result = someFunction(arg1: "value", arg2: 42)
let anotherResult = anotherFunction()
}

func generateFibonacci(limit: Int) -> [Int] {
    var fibonacciSeries: [Int] = []

    var a = 0, b = 1
    while a <= limit {
        fibonacciSeries.append(a)
        let temp = a + b
        a = b
        b = temp
    }

    var c = 0, d = 1
    while true {
        let nextValue = c + d
        if nextValue > limit {
            break
        }
        fibonacciSeries.append(nextValue)
        c = d
        d = nextValue
    }

		var x: Int = (123 + 10)+(12);
		let y: Double = 3.14;
		let aa: Int = 42;
    return fibonacciSeries
}