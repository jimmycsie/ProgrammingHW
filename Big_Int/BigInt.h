#include <string>

class BigInt{
	
	private:
		string name;
		string integer;
	    	    
	public:
		BigInt();                                              //default constructor
		BigInt(const string integer);                      
		BigInt(const string name, const string integer);
		BigInt(const BigInt& w);                               //copy constructor
		~BigInt();                                             //destructor
		void print() const;                                    //print the value of BigInt
		const string& getName() const;                         //get the name of BigInt 
		bool operator==(const BigInt& w) const;            
		bool operator!=(const BigInt& w) const;
		const BigInt& operator=(const string& a);       
		const BigInt& operator=(const BigInt& w);       
		const BigInt& operator+=(BigInt w);                    //the sum of BigInt
		const BigInt operator+(const BigInt& w) const;         //the sum of BigInt
 		const BigInt operator-() const;                        //unary operator of BigInt
 		const BigInt& operator+() const;                       //unary operator of BigInt    
		const BigInt operator-(const BigInt& w) const;         //the difference of BigInt
		const BigInt& operator*=(const char n);                //BigInt multiply a single digit
		const BigInt operator*(const char n) const;            //BigInt multiply a single digit
		const BigInt& operator*=(BigInt w);                    //BigInt multiply BigInt
		const BigInt operator*(const BigInt& w) const;         //BigInt multiply BigInt
    		const BigInt& operator/=(BigInt w);                    //BigInt divide BigInt, take the integer onl
		const BigInt operator/(const BigInt&  w) const;        //BigInt divide BigInt, take the integer only
 		const BigInt operator%(const BigInt w) const;          //BigInt divide BigInt, take the remainder only
		const BigInt square() const;                           //the square of BigInt
		const BigInt abs() const;                              //the absolute of BigInt
		int operator[](int i) const;                           //get the i-th digit
		bool isPrime() const;                                  //determine whether the BigInt is a prime number, using Fermat Primality test
		BigInt montgomery(BigInt exp, BigInt mod);             //count (BigInt^(exp))%mod, using montgomery
}; 


#endif
