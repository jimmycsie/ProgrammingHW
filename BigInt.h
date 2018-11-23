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
    	const BigInt& operator/=(BigInt w);                    //BigInt divide BigInt, take the integer only
    	const BigInt operator/(const BigInt&  w) const;        //BigInt divide BigInt, take the integer only
    	const BigInt operator%(const BigInt w) const;          //BigInt divide BigInt, take the remainder only
    	const BigInt square() const;                           //the square of BigInt
    	const BigInt abs() const;                              //the absolute of BigInt
    	int operator[](int i) const;                           //get the i-th digit
    	bool isPrime() const;                                  //determine whether the BigInt is a prime number, using Fermat Primality test
    	BigInt montgomery(BigInt exp, BigInt mod);             //count (BigInt^(exp))%mod, using montgomery
    	
}; 







//------------------------ BigInt member functions -------------------- //

BigInt::BigInt(){
	name = "NO_NAME";
	integer = "0";
}
BigInt::BigInt(const string integer){
	name = "NO_NAME";
	this->integer = integer;
} 
BigInt::BigInt(const string name, const string integer){
	this->name = name;
	this->integer = integer;
}
BigInt::BigInt(const BigInt& w){
	this->integer = w.integer ;
} 
BigInt::~BigInt(){
;
}
void BigInt::print() const{
	for(int i=0 ; i<integer.length();i++)
		cout<<integer[i];
	cout<<"\n";
}
const string& BigInt::getName() const{
	return name;
}
bool BigInt::operator==(const BigInt& w) const{
	if(this->integer == w.integer)
		return true;
	return false;
}
bool BigInt::operator!=(const BigInt& w) const{
	if(this->integer != w.integer)
		return true;
	return false;
}
const BigInt& BigInt::operator=(const string& a){
	this->integer = a;
	return *this;
}
const BigInt& BigInt::operator=(const BigInt& w){
	this->integer = w.integer ;
	return *this;
}
const BigInt& BigInt::operator+=(BigInt w){
	bool negative1=false, negative2=false;
	if(integer[0]=='-'){
		negative1=true;
		integer.erase(0,1);
	}
	if(w.integer[0]=='-'){
		negative2=true;
		w.integer.erase(0,1);
	}
	
	int length1=integer.length();          //將位數變相同 
	int length2=w.integer.length();
	if(length1>length2){
		for(int i=0;i<length1-length2;i++)
	    	w.integer.insert(0,"0");
	}	
	else if(length1<length2){
	    	for(int i=0;i<length2-length1;i++)
	   		integer.insert(0,"0");
	}
    	length1=integer.length();          
	length2=w.integer.length();    

	//--------------------正正相加，負負相加-------------- 
	if(negative1==negative2){           
		int carry=0;	    
		for(int i=length1-1 ; i>=0 ; i--){
	        	int sum=0;
		        if(w.integer[i]-'0' + this->integer[i]-'0' + carry >=10){
		        	sum = -10 + carry;
		        	carry=1;  	
			}
		  	else{
				sum = carry;
			        carry=0;
		        }
		        sum = sum + w.integer[i]-'0'+this->integer[i]-'0';
		        this->integer[i] = sum + '0';  
			if(i==0 && carry==1)
				this->integer.insert(0,"1") ;  
        	} 
		if(negative1==true){
    			this->integer.insert(0,"-");
    			w.integer.insert(0,"-");
		} 
		return *this;		
	}

    //--------------------一正一負---------------
	else{						  //negative1 != negative2
		int borrow=0;
		bool PlusNeg=false;
		BigInt BigNum, SmallNum;
		if(integer.compare(w.integer)>=0){        //此時長度已經一樣 
			BigNum = *this;
			SmallNum = w;
			if(negative1==true)
				PlusNeg=true;
		}
		else if(integer.compare(w.integer)<0){
			BigNum = w;
			SmallNum = *this;
			if(negative2==true)
				PlusNeg=true;
		}
		
		if(BigNum == SmallNum){
			*this="0";		 
	    		return *this;
		}
		for(int i=length1-1;i>=0;i--){
            		int subtract=0;		    
			if(BigNum.integer[i]-borrow < SmallNum.integer[i]){
		        	subtract = 10-borrow;   
	    			borrow=1;     
			}	
			else{
			 	subtract = -borrow;
			 	borrow=0;
			}	 
			subtract = subtract + BigNum.integer[i] - SmallNum.integer[i];  //相減，所以不用減 '0' 
			BigNum.integer[i]=subtract+'0';
		}
			 
		while(BigNum.integer.length()!=1 && BigNum.integer[0]=='0')
	        	BigNum.integer.erase(0,1);
		if(PlusNeg==true)
			BigNum.integer.insert(0,"-");
		*this=BigNum;		 
		return *this;	
	} 
}
const BigInt BigInt::operator+(const BigInt& w) const{
	BigInt sum(w);
	sum += *this;
	return sum;
} 
const BigInt BigInt::operator-() const{
	BigInt Negative(*this);
	BigInt zero("0");
	if(Negative.integer[0]!='-' && Negative!=zero)
       		Negative.integer.insert(0,"-");
    	else if(Negative.integer[0]=='-')
        	Negative.integer.erase(0,1);
    	return Negative;
}
const BigInt& BigInt::operator+() const{
	return *this;
}
const BigInt BigInt::operator-(const BigInt& w) const{
 	BigInt subtract(*this);
    	subtract += (-w);
 	return subtract;
}
const BigInt& BigInt::operator*=(char n){
	if(integer[0]=='-'){
		cout<<"cannot multiply int to negative"<<"\n";
		return *this;
	}
	if(integer[0]=='0' || n=='0'){
		this->integer = "0";
		return *this;
	}
	int carry=0,multiply=0;
	int num=n-'0';
	for(int i=integer.length()-1;i>=0;i--){
		multiply = (num*(integer[i]-'0')+carry)%10;  //取個位數 
		carry = (num*(integer[i]-'0')+carry)/10;     //取十位數 
		integer[i]=multiply+'0';
		if(i==0 && carry!=0)
			this->integer.insert(0,1,carry+'0');	    
	}  
	
	return *this;
}
const BigInt BigInt::operator*(const char n) const{
 	BigInt multiple(*this);
	multiple *= n;
	return multiple;
} 
const BigInt& BigInt::operator*=(BigInt w){
	bool negative1=false, negative2=false;
	BigInt sum;
	BigInt multiple;
	if(integer[0]=='-'){
		negative1=true;
		integer.erase(0,1);
	}
	if(w.integer[0]=='-'){
		negative2=true;
		w.integer.erase(0,1);
	}
	
	for(int i=w.integer.length()-1;i>=0;i--){
		multiple = *this * w.integer[i];
		for(int j=i;j<w.integer.length()-1;j++)
			multiple.integer.push_back('0');
		sum += multiple;
	}
	*this = sum;
	if((negative1 != negative2) && this->integer[0]!='0')
		this->integer.insert(0,"-");
	while(this->integer.length()!=1 && this->integer[0]=='0')
		this->integer.erase(0,1);
	return *this;
}
const BigInt BigInt::operator*(const BigInt& w) const{
	BigInt multiple(*this);
	multiple *= w;
	return multiple; 
}
const BigInt& BigInt::operator/=(BigInt w){   
	bool negative1=false, negative2=false;  
	bool start=false;
	string quotient;
	if(integer[0]=='-'){
		negative1=true;
		integer.erase(0,1);
	}
	if(w.integer[0]=='-'){
		negative2=true;
		w.integer.erase(0,1);
	}
	
	if( (w.integer.length() > this->integer.length())
		|| ((w.integer.length() == this->integer.length()) && (w.integer>this->integer))){
		// check if 除數 > 被除數
		*this="0";
		return *this; 
	}
			    
	BigInt divide(w);
	for(int i=0;i<integer.length()-1;i++)
		divide.integer.push_back('0');
   
	int Length = this->integer.length(); // *this 的長度會被改到 
	for(int i=0;i<Length;i++){	
		int value=0;
		for(int j=1;j<=10;j++){  //當超過時跳出，因此 j<=10 
			if( ((divide*(j+'0')).integer.length() > this->integer.length())
			    || (((divide*(j+'0')).integer.length() == this->integer.length()) && ((divide*(j+'0')).integer > this->integer))){
				value=j-1;	
				// 當乘出來的數 > this->integer 時		
				break;
			}
		}
		if(value==0 && start==false){
			divide.integer.pop_back();
			continue;	
		}
		start=true;
		quotient += (value+'0');
		*this = *this - (divide*(value+'0'));
		divide.integer.pop_back();
	}	
	*this = quotient;
	if(negative1!=negative2)
		this->integer.insert(0,"-");
	return *this;
}
const BigInt BigInt::operator/(const BigInt& w) const{
	BigInt divide(*this);
	divide /= w;
	return divide;
} 
const BigInt BigInt::operator%(const BigInt w) const{
	BigInt quotient(*this);
	BigInt remainder;
	quotient /= w ;
	remainder = *this - (quotient * w);
	return remainder;
}
const BigInt BigInt::square() const{
	BigInt squ(*this);
	squ *= *this;
	return squ;
}
const BigInt BigInt::abs() const{
	BigInt positive(*this);
	if(this->integer[0]=='-')
        positive.integer.erase(0,1);
	return positive;
}
int BigInt::operator[](int i) const{
	if(i<0 || i >= this->integer.length() || integer[integer.length()-1-i]=='-')
        	return -1;
    	return this->integer[integer.length()-1-i]-'0';
}
bool BigInt::isPrime() const{             //Fermat primality test
	
	/* 
		The Fermat primality test is a probabilistic test to determine whether a number is a probable prime.
		if n is a prime, for every 1 < a < n-1, then a^(n-1) mod n = 1	
		if n is not a prime, then a^(n-1) mod n may be 1 ()
	*/	
	
	const int dataNum=25;
	BigInt base[dataNum];
	base[0]="2"; base[1]="3"; base[2]="5"; base[3]="7"; base[4]="11";
	base[5]="13"; base[6]="17"; base[7]="19"; base[8]="23"; base[9]="29";
	base[10]="31"; base[11]="37"; base[12]="41"; base[13]="43"; base[14]="47";
	base[15]="53"; base[16]="59"; base[17]="61"; base[18]="67"; base[19]="71";
	base[20]="73"; base[21]="79"; base[22]="83"; base[23]="89"; base[24]="97";
	//---------------------------------------------------------------------------

    
	BigInt one("1");
	BigInt test,random;
	srand(time(nullptr));
	int rn=0;
	char num[10];
	string temp;	
	if(*this==one)
		return false;
	for(int i=0;i<dataNum;i++){
		if(*this==base[i])
			return true;
	}
	for(int i=0;i<dataNum;i++){
	 	test = base[i].montgomery(*this-one,*this);
		if(test != one){
			return false;	
		}
		     
	}
	return true;    
}
BigInt BigInt::montgomery(BigInt exp, BigInt mod){
	BigInt two("2");
	BigInt one("1");
	BigInt value;
	if(exp == one)
		return *this % mod;
	else if(exp == two)
		return *this * *this % mod;
	else if((exp % two).integer == "0"){	
		value = this->montgomery(exp/two, mod);
		return (value*value) % mod;
	}
	else{
		value = this->montgomery((exp-one)/two, mod);
		return (value*value* *this) % mod;
	}
}

