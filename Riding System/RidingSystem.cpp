#include <iostream>
#include <vector>
#include <string>
#include <stdlib.h>
#include <stdexcept> 
using namespace std;


class matchUp{
	private:
	    int ComScore;
	    int distance;
	    int order;
	public:
		matchUp();
		matchUp(int ComScore,int distance,int order);
		bool operator>(const matchUp& m) const;
		const matchUp& operator=(const matchUp& m);
		void print() const;
};
struct satisfy{
	short score=0;
	int money=0;
	int distance=0;
}; 

class Entity{
	protected:
		bool isOnline;
		bool isService;   
		bool isOnboard;
		int x_coordinate;
	    int y_coordinate; 
	    vector<string> characteristic;
		void applyLocation(string& time);
	public:
		bool getOnline() const;
	    bool getService() const;
	    bool getOnboard() const;
	    virtual void CompelOffline();
	    virtual string& getName()=0;
};

class Passenger : public Entity{
	friend satisfy grading(Passenger* caller, string& time, string& location, int tagCount, bool isRegular);
	private:
		string phone;
		string Cname;
		short onlineTime;
		short onboardTime;
	    void applyTime(string& time);
	public:
		Passenger();
		Passenger(const Passenger& p);
		Passenger(const string& phone,string& tag);  //format of tag (...,...,...)  constructure 註冊新成員  
        char getName(int i) const;
        string& getName();
		vector<string> getTag() const;
		int getX() const;
		int getY() const;
		void print() const;
		void online(string& time, string& location) throw(logic_error);
        void watingCar(string name) throw(logic_error);
        void onBoard(string& time) throw(logic_error);
        void offline() throw(logic_error);
        void CompelOffline();
        void getState() const;
        
};

class Car : public Entity{
	static int apply;
	friend matchUp* match(Car* driver, Passenger* caller, string& time,
	                      int Max_dis, int idealScore, int tagScore, int disWeighted);
	private:
	    string name;
	    int tagWithP;       //tag count same with passenger, note that the number is correct if and only if there is passenger on the car.
		short time;         // minute mean time  ex:13點15分 為  13*60+15=795 
	    char direction;      //Halt for H, East for E, West for W, South for S, North for N
	    short speed;         //1 for regular car, 2 for luxury car
	    int GetScoreCount;
	    int score;
	    string Pnumber;
	    int order;             //registration order
        void applyTime(string& time);
	public:
	    Car();	    
	    Car(const Car& c);
	    Car(const string& name,string& tag,char isRegular); //format of tag (...,...,...)  constructure 註冊新車子 
	    char getName(int i) const;
	    string& getName() ;
	    string& getP() ;
	    int getTagWithP() const;
		bool isRegular() const;
		void print() const;
	    void online(string& time,string& location, char direction)  throw(logic_error); // ("13:15",(87,40),H)
	    void ChangeDir(string& time, char direction) throw(logic_error);
	    void BoundtoP(string& number) throw(logic_error);
		void POnBoard() throw(logic_error);
	    void arrival(string& time,string& location, char direction) throw(logic_error);
	    void CompelOffline();
		void offline() throw(logic_error);
	    void addScore(short i);
	    void getState(string& time);
};
int Car::apply=1;

template<typename TypeName>   //Car or Person
class Node{
    //private:
	public:
		char key;
		TypeName* object;
		vector<Node<TypeName>*> children;
		Node<TypeName>* parent;	
//	public:		
		Node();     
		Node(char key);  
		Node(TypeName& object, int level);  //TypeName need a memeber function of getName
};

template<typename TypeName> 
class Bag{               //sorting by string. Hence TypeName must have getName() 
	private:
		vector<Node<TypeName>*> header;
		int ItemCount;
		Node<TypeName>* findNode(string& name);
		vector<TypeName*> depth_first_search(Node<TypeName>* p);
		
	public:
		Bag(); 
		Bag(const Bag& t);           
		~Bag();
		void add(TypeName& NewEntry);
		TypeName* search(string& name);
		TypeName* remove(string& name) throw(logic_error);	
		vector<TypeName*> traversal(); 
		bool isEmpty();
		void clear();
}; 


//------------------global function -----------------------------
matchUp* match(Car* driver, Passenger* caller, string& time,
               int Max_dis, int idealScore, int tagScore, int disWeighted);
Car* applyCar(Bag<Car>& emptyLorR, Passenger* calling, string& time, 
              int Max_dis, int idealScore, int tagScore, int disWeighted);
satisfy grading(Passenger* caller, string& time, string& location, int tagCount, bool isRegular);
//----------------------------------------------------------------

int main(){
	//storing four data structure. 
	//one for all car registration, and all passenger, respectively. 
	//one for luxury empty online car, and regular empty onling car, respectively.
	//using search to search or  modify a object.
	//using traversal to get a vector to search or modify all luxuary/regular empty online car.
	int Max_dis=0,Rintercept=0,Rslope=0,Lintercept=0,Lslope=0;
	int idealScore=0,tagScore=0,disWeighted=0,tagCount=0;
	cin>>Max_dis>>Rintercept>>Rslope>>Lintercept>>Lslope
	   >>idealScore>>tagScore>>disWeighted>>tagCount;
	string tag;  //其實後面沒用到 
	cin.ignore(1);     //ignore '\0'
	std::getline(std::cin,tag);
    tag="";
    
    //--------------------variable and data structures----------------
	string command,characteristic,phone,name,time,location;
	char LorR='\0',direction='\0';
	int sum=0;
	Passenger* Pmember;   //新增會員
	Passenger* SearchP = nullptr; 
	Car* Cmember;  //新增車子 
	Car* SearchC = nullptr;
	vector<Car*> allCarInVector;
	vector<Passenger*> allPInVector;
	Bag<Passenger> allPassenger;
	Bag<Car> allCar, emptyL, emptyR;
	//---------------------------------------------------------------
	
	while(std::getline(std::cin,command)){        //[6][7] are the command
		if(command[6]=='N' && command[7]=='P'){  //新乘客註冊  
		    //條件:沒有註冊過 
        	phone=command.substr(9,10);
            SearchP=allPassenger.search(phone);
		    if(SearchP!=nullptr)
		        continue; 
			characteristic=command.substr(command.find('('));	
			Pmember = new Passenger(phone, characteristic);
            allPassenger.add(*Pmember);
            SearchP=nullptr;
		}
		else if(command[6]=='N' && command[7]=='C'){  //新車子註冊 
		    //條件:沒有註冊過 
        	name=command.substr(9,6);
        	SearchC=allCar.search(name);
		    if(SearchC!=nullptr)
			    continue;
			LorR=command[command.length()-1];
        	command.pop_back();
			characteristic=command.substr(command.find('('));	
            Cmember = new Car(name, characteristic, LorR);
            allCar.add(*Cmember);
            SearchC=nullptr;
		}
		else if(command[6]=='O' && command[7]=='C'){   //車子上線 
		    //條件:已註冊過 尚未上線
			name=command.substr(9,6);
			SearchC=allCar.search(name);
		    if(SearchC==nullptr || SearchC->getOnline()==true)
			    continue;
        	time=command.substr(0,5);
        	direction=command[command.length()-1];
        	command.pop_back();
        	location=command.substr(15);  	
        	SearchC->online(time, location, direction);
        	if(SearchC->isRegular()==true)
        	    emptyR.add(*SearchC);
        	else
        	    emptyL.add(*SearchC);
        	SearchC=nullptr;
		}
		else if(command[6]=='O' && command[7]=='P'){   //乘客上線 
			//條件: 已註冊過 尚未上線
			phone=command.substr(9,10);
            SearchP=allPassenger.search(phone);
		    if(SearchP==nullptr || SearchP->getOnline()==true)
		        continue; 
			LorR=command[command.length()-1];
			command.pop_back();
			location=command.substr(19);
			time=command.substr(0,5);
			SearchP->online(time,location); 
			Car* getCar;
			if(LorR=='L')
			    getCar = applyCar(emptyL,SearchP,time,Max_dis,idealScore,tagScore,disWeighted);
		    else
		        getCar = applyCar(emptyR,SearchP,time,Max_dis,idealScore,tagScore,disWeighted);
		    if(getCar!=nullptr){
		    	getCar->BoundtoP(phone);
		    	SearchP->watingCar(getCar->getName());
		    	if(LorR=='L')
		    	    emptyL.remove(getCar->getName());
		    	else
		    	    emptyR.remove(getCar->getName());
			}
			else
			    SearchP->offline();
			SearchP=nullptr;
		}	
		else if(command[6]=='C' && command[7]=='P'){   //車子接到乘客 
			//條件: 車子->已註冊過 上線中 服務中狀態 車上無乘客
			//      乘客->已註冊過 上線中 等待中
			name=command.substr(9,6);
			SearchC=allCar.search(name);  
			if(SearchC!=nullptr)
			    SearchP=allPassenger.search(SearchC->getP());
			else
			    continue;
			if(SearchC->getOnline()==false || SearchC->getService()==false || SearchC->getOnboard()==true
			   || SearchP==nullptr || SearchP->getOnline()==false || SearchP->getService()==false || SearchP->getOnboard()==true)
			    continue; 
			
			time=command.substr(0,5);
			SearchC->POnBoard();
			SearchP->onBoard(time);
			SearchC=nullptr;
			SearchP=nullptr;
		}
		else if(command[6]=='A' && command[7]=='D'){   //抵達目的地 
	        //車子已註冊過 服務中 載客中
			name=command.substr(9,6);
			SearchC=allCar.search(name);
		    if(SearchC==nullptr || SearchC->getOnline()==false || SearchC->getService()==false || SearchC->getOnboard()==false)
			    continue;		
			time=command.substr(0,5);
        	direction=command[command.length()-1];
        	command.pop_back();
        	location=command.substr(15);
        	string location1=location;
			if(SearchC->isRegular()==true)
			    emptyR.add(*SearchC);
			else
			    emptyL.add(*SearchC);
			
			satisfy p;
			SearchP=allPassenger.search(SearchC->getP());
			p=grading(SearchP,time,location,SearchC->getTagWithP(),SearchC->isRegular());
		    SearchC->addScore(p.score);
		    if(p.money!=-1){
		    	if(SearchC->isRegular()==true)
		    	    sum += (Rintercept+Rslope*p.distance);
		    	else
		    	    sum += (Lintercept+Lslope*p.distance);
			}
			SearchC->arrival(time,location1,direction);
			SearchP->offline();
			SearchC=nullptr;
			SearchP=nullptr;   
		} 
		else if(command[6]=='E' && command[7]=='C'){   //空車改變移動方向
		    //條件: 已註冊過 上線 空車
			name=command.substr(9,6);
			SearchC=allCar.search(name);
		    if(SearchC==nullptr || SearchC->getOnline()==false || SearchC->getService()==true)
			    continue; 
			time=command.substr(0,5);
			direction=command[command.length()-2];
			SearchC->ChangeDir(time, direction);
			SearchC=nullptr;
	    }
		else if(command[6]=='L' && command[7]=='C'){   //車子離線 
			name=command.substr(9,6);
			SearchC=emptyR.search(name);     //車子上線且為未服務狀態才找的到 
			if(SearchC==nullptr){
				SearchC=emptyL.search(name);
			    if(SearchC==nullptr){
				    continue;
			    }
			    else
			        emptyL.remove(name);
		    }
			else
			    emptyR.remove(name);  
			SearchC->offline();
			SearchC=nullptr;
		}
		else if(command[6]=='S' && command[7]=='C'){   //查詢車子 
	        name=command.substr(9,6);
	        time=command.substr(0,5);
	        SearchC=allCar.search(name);
		    if(SearchC!=nullptr)
		    	SearchC->getState(time);
			else
			    cout<<name<<": no registration!"<<"\n";
		    SearchC=nullptr;
		} 
		else if(command[6]=='S' && command[7]=='P'){   //查詢乘客 
	        phone=command.substr(9,10);
	        SearchP=allPassenger.search(phone);
		    if(SearchP!=nullptr)
		    	SearchP->getState();
			else
			    cout<<phone<<": no registration!"<<"\n";
		    SearchP=nullptr;
		} 
		else if(command[6]=='S' && command[7]=='R'){   //查詢平台收益 
			cout<<sum<<"\n";
		}
		else if(command[6]=='Z' && command[7]=='Z'){   //系統當機 
		    allCarInVector=allCar.traversal();
		    allPInVector=allPassenger.traversal();
			for(int i=0;i<allCarInVector.size();i++)
				allCarInVector[i]->CompelOffline(); 
				
			for(int i=0;i<allPInVector.size();i++)
			    allPInVector[i]->CompelOffline();
			emptyR.clear();
			emptyL.clear();    	    
		} 
		command="        ";
	}
	
	//記得delete 
	return 0;
}




matchUp::matchUp(){
    ComScore=0;
	distance=0;
	order=0;
}
matchUp::matchUp(int ComScore,int distance,int order){
	this->ComScore=ComScore;
	this->distance=distance;
	this->order=order;
}
bool matchUp::operator>(const matchUp& m) const{
	if(ComScore>m.ComScore || (ComScore==m.ComScore && distance<m.distance)
	   || (ComScore==m.ComScore && distance==m.distance && order<m.order))
		return true;
	return false;
}
const matchUp& matchUp::operator=(const matchUp& m){
	this->ComScore=ComScore;
	this->distance=distance;
	this->order=order;
}
void matchUp::print() const{
	cout<<this->ComScore<<" ";
}

void Entity::applyLocation(string& location){
	string x,y;
	location.pop_back();
	y=location.substr(location.find_last_of(",")+1);
	while(location[location.length()-1]!=',')
	    location.pop_back();
	location.pop_back();
	x=location.substr(location.find_last_of("(")+1);	
	this->x_coordinate=stoi(x,nullptr,10);  //throw invalid_argument, out_of_range
	this->y_coordinate=stoi(y,nullptr,10);
}
bool Entity::getOnline() const{
	return isOnline;
}
bool Entity::getService() const{
	return isService;
}
bool Entity::getOnboard() const{
    return this->isOnboard;
}
void Entity::CompelOffline(){
	this->isOnline=true;
	this->isService=false;
	this->isOnboard=false;
}

Car::Car(){
	name="";
	isOnline=false;
	isService=false;
	isOnboard=false;
	tagWithP=0;
	time=0;
	x_coordinate=0;
	y_coordinate=0;
	direction='\0';
	speed=0;
	GetScoreCount=0;
	score=0;
	Pnumber=""; 
	order=0;
}
Car::Car(const Car& c){
	this->name=c.name;
	this->isOnline=c.isOnline;
	this->isService=c.isService;
	this->isOnboard=c.isOnboard;
	this->characteristic=c.characteristic;
	this->tagWithP=c.tagWithP;
	this->time=c.time;
	this->x_coordinate=c.y_coordinate;
	this->y_coordinate=c.x_coordinate;
	this->direction=c.direction;
	this->speed=c.speed;
	this->GetScoreCount=c.GetScoreCount;
	this->score=c.score;
	this->Pnumber=c.Pnumber;
	this->order=c.order;
}
Car::Car(const string& name,string& tag,char isRegular){
	this->name=name;    //format of string (...,...,...)
	if(tag[0]!='(' || tag[tag.length()-1]!=')' )
	    ;//throw eception	
	    
	while(tag.length()>1){
	    tag.pop_back();     //delete ) or ,
	    if(tag[tag.size()-1]!='(') 
	        this->characteristic.push_back(tag.substr(tag.find_last_of(",(")+1));
	    while(tag[tag.size()-1]!=',' && tag[tag.size()-1]!='(')
	        tag.pop_back();
    }
    if(isRegular=='R')
        this->speed=1;
    else
        this->speed=2;
	isOnline=false;
	isService=false;
	isOnboard=false;
	tagWithP=0;
	x_coordinate=0;
	y_coordinate=0;
	direction=0;
	GetScoreCount=0;
	score=0;
	Pnumber="";
	this->order=this->apply;
	this->apply++;
}
char Car::getName(int i) const{
	if(i<name.length() || i>=0)
	    return name[i];
	return '\0';
}
string& Car::getName(){
    return name;
}
string& Car::getP(){
	return this->Pnumber;
}
void Car::applyTime(string& time){
	char hour[3],minute[3];
	hour[0]=time[0];hour[1]=time[1];hour[2]='\0';
	minute[0]=time[3];minute[1]=time[4];minute[2]='\0';
	short h=0,min=0;
	h=atoi(hour);
	min=atoi(minute);
	this->time=h*60+min;
}
int Car::getTagWithP() const{
    return tagWithP;
}
bool Car::isRegular() const{
	if(speed==1)
	    return true;
	return false;
}
void Car::print() const{
    cout<<name<<"\n";
}
void Car::online(string& time,string& location, char direction) throw(logic_error){  //("13:15",(87,40),H)
	if(isOnline==true || isService==true || isOnboard==true)
	    throw logic_error("Using online only when the car is offline");
	applyTime(time);
	applyLocation(location);
	this->direction=direction;
	isOnline=true;
	isService=false;
	isOnboard=false;
	tagWithP=0;
	Pnumber=""; 	
}
void Car::ChangeDir(string& time, char direction) throw(logic_error){    //("13:15",N)
	if(isOnline==false || isService==true || isOnboard==true)
	    throw logic_error("Using ChangeDir only when the car is online and empty");
	short temp=this->time,displacement=0;
	applyTime(time);
	displacement = (this->time-temp)*speed;
	if(this->direction=='E')
	    this->x_coordinate += displacement;
	else if(this->direction=='W')
	    this->x_coordinate -= displacement;
	else if(this->direction=='S')
	    this->y_coordinate -= displacement;
	else if(this->direction=='N')
	    this->y_coordinate += displacement;
	  
	if(direction!='\0')    
	    this->direction=direction;
}
void Car::BoundtoP(string& number) throw(logic_error){
	if(isOnline==false || isService==true || isOnboard==true)
	    throw logic_error("Using BoundToP only when the car is online and empty");
	isService=true;
	this->Pnumber=number;
}
void Car::POnBoard() throw(logic_error){
	if(isOnline==false || isService==false || isOnboard==true)
	    throw logic_error("Using POnBoard only when the car is online and servicing without passenger");
	isOnboard=true;
}
void Car::arrival(string& time,string& location, char direction) throw(logic_error){
	if(isOnline==false || isService==false || isOnboard==false)
	    throw logic_error("Using arrival only when the car is online and servicing with passenger");
	this->isService=false;
	this->isOnboard=false;
	this->offline();
	this->online(time,location,direction);
	this->Pnumber="";
}
void Car::offline() throw(logic_error){
	if(isOnline==false || isService==true || isOnboard==true)
	    throw logic_error("Using offline only when the car is online and non-service");
	if(isService==true)
	;//throw exceptional
	this->isOnline=false;
	this->isService=false;
	this->isOnboard=false;
	this->tagWithP=0;
	this->time=0;
	this->x_coordinate=0;
	this->y_coordinate=0;
	this->direction='\0';
	this->Pnumber=""; 
}
void Car::CompelOffline(){
	Entity::CompelOffline();
	this->offline();
}
void Car::addScore(short i){   
	this->score += i;
	this->GetScoreCount++;
}
void Car::getState(string& time){    //("13:15")
	short state=-1;
	if(isOnline==false && isService==false && isOnboard==false)
	    state=0;
	else if(isOnline==true && isService==false && isOnboard==false)
	    state=1;
	else if(isOnline==true && isService==true && isOnboard==false)
	    state=2;
	else if(isOnline==true && isService==true && isOnboard==true)
	    state=3;
	else
	    cout<<"state error";    
	cout<<name<<" "<<state<<" "<<GetScoreCount<<" "<<score;
 
	switch(state){
		case 1:this->ChangeDir(time,this->direction);
		       cout<<" "<<x_coordinate<<" "<<y_coordinate; break;
		case 2:
		case 3:cout<<" "<<Pnumber; break;
	}
	cout<<"\n";
}


Passenger::Passenger(){
	this->phone="";
	this->Cname="";
	this->isOnline=false;
	this->isService=false;
	this->isOnboard=false;
	this->onlineTime=0;
	this->onboardTime=0;
	this->x_coordinate=0;
    this->y_coordinate=0;
} 
Passenger::Passenger(const Passenger& p){
	this->phone = p.phone;
	this->Cname = p.Cname;
	this->isOnline = p.isOnline;
	this->isService = p.isService;
	this->isOnboard = p.isOnboard;
	this->onlineTime = p.onlineTime;
	this->onboardTime = p.onboardTime;
	this->characteristic = p.characteristic;
	this->x_coordinate = p.x_coordinate;
	this->y_coordinate = p.y_coordinate;
}
Passenger::Passenger(const string& phone,string& tag){
	this->phone=phone;    //format of string (...,...,...)
	if(tag[0]!='(' || tag[tag.length()-1]!=')' )
	    ;//throw eception	
	    
	while(tag.length()>1){
	    tag.pop_back();     //delete ) or ,
	    this->characteristic.push_back(tag.substr(tag.find_last_of(",(")+1));
	    while(tag[tag.size()-1]!=',' && tag[tag.size()-1]!='(')
	        tag.pop_back();
    }
    this->Cname="";
    this->isOnline=false;
	this->isService=false;
	this->isOnboard=false;
	this->onlineTime=0;
	this->onboardTime=0;
	this->x_coordinate=0;
    this->y_coordinate=0;
} 
void Passenger::applyTime(string& time){
	char hour[3],minute[3];
	hour[0]=time[0];hour[1]=time[1];hour[2]='\0';
	minute[0]=time[3];minute[1]=time[4];minute[2]='\0';
	short h=0,min=0;
	h=atoi(hour);
	min=atoi(minute);
	if(isOnline==false && isService==false && isOnboard==false){
		this->onlineTime=h*60+min;
		this->onboardTime=0;
	}
	else if(isOnline==true && isService==true && isOnboard==false)
	    this->onboardTime=h*60+min;
}
char Passenger::getName(int i) const{
	if(i<phone.length() || i>=0)
	    return phone[i];
	return '\0';
}
string& Passenger::getName(){
    return phone;
}
vector<string> Passenger::getTag() const{
    return this->characteristic;
}
int Passenger::getX() const{
    return this->x_coordinate;
}
int Passenger::getY() const{
    return this->y_coordinate;
} 
void Passenger::print() const{
    cout<<this->phone<<"\n";
}
void Passenger::online(string& time, string& location) throw(logic_error){
	if(isOnline==true || isService==true || isOnboard==true)
	    throw logic_error("Using online only when the passenger is offline");
	applyTime(time);
	applyLocation(location);
	isOnline=true;
	isService=false;
	isOnboard=false;
}
void Passenger::watingCar(string name) throw(logic_error){
	if(isOnline==false || isService==true || isOnboard==true)
	    throw logic_error("Using waitingCar only when the passenger is online and non-service");
	this->Cname=name;
	isService=true;
}
void Passenger::onBoard(string& time) throw(logic_error){
	if(isOnline==false || isService==false || isOnboard==true)
	    throw logic_error("Using onBoard only when the passenger is online and waiting car");
	applyTime(time);
	isOnboard=true;
}
void Passenger::offline() throw(logic_error){
	if(isOnline==false || (isService==true && isOnboard==false) || (isService==false && isOnboard==true))
	    throw logic_error("Using offline only when the passenger is online and non-service or after Onboard");

	this->Cname="";
	this->isOnline=false;
	this->isService=false;
	this->isOnboard=false;
	this->x_coordinate=0;
    this->y_coordinate=0;
    this->onlineTime=0;
	this->onboardTime=0;
}
void Passenger::CompelOffline(){
	Entity::CompelOffline();
	this->offline();
}
void Passenger::getState() const{
	short state=-1;
	if(isOnline==false && isService==false && isOnboard==false)
	    state=0;
	else if(isOnline==true && isService==true && isOnboard==false)
	    state=1;
	else if(isOnline==true && isService==true && isOnboard==true)
	    state=2;
	else
	    cout<<"state error";    
	cout<<phone<<" "<<state;
	
	switch(state){
		case 1:
		case 2:cout<<" "<<Cname; break;
	}
	cout<<"\n";
}

template<typename TypeName>
Node<TypeName>::Node(){
	this->key='\0';
	this->object=nullptr;
	this->parent=nullptr;
}
template<typename TypeName>
Node<TypeName>::Node(char key){
	this->object = nullptr;
	this->parent = nullptr;
	this->key=key;
}
template<typename TypeName>
Node<TypeName>::Node(TypeName& object, int level){
	this->parent = nullptr;
	if(object.getName(level)!='\0'){
		this->key = object.getName(level);
		this->object = nullptr;
	}
	else{
		this->key = '\0';
		this->object = &object;
	} 
}

template<typename TypeName>
Bag<TypeName>::Bag(){
	this->ItemCount=0;
}
template<typename TypeName>
Bag<TypeName>::~Bag(){
	this->clear();
}
template<typename TypeName>
Bag<TypeName>::Bag(const Bag& t){    //the copy constructure only do shallow copy
	this->header=t.header;
	this->ItemCount=t.ItemCount;	
}
template<typename TypeName>            
void Bag<TypeName>::add(TypeName& NewEntry){
	bool get=false;
	Node<TypeName>* ptr=nullptr;
    Node<TypeName>* newNode;
	for(int i=0;i<header.size();i++){                 //determine the first letter
		if(header[i]->key==NewEntry.getName(0)){
			ptr = header[i];
			get=true;
			break;
		}		    
	}
	if(get==false){
		newNode =  new Node<TypeName>(NewEntry,0);	
		header.push_back(newNode);
		ptr = header[header.size()-1];
	    
	}	
	get=false;
	int i=1;
	while(NewEntry.getName(i)!='\0'){
		for(int j=0;j<ptr->children.size();j++){
			if(ptr->children[j]->key == NewEntry.getName(i)){
	    	    ptr = ptr->children[j];
	    	    get=true;	    	    
	    	    break;
		    }
		}
		if(get==false){
			newNode =  new Node<TypeName>(NewEntry,i);
			newNode->parent = ptr;
			ptr->children.push_back(newNode);               //在vector最後面push_back 
	        ptr = ptr->children[ptr->children.size()-1];   //將ptr指向該node 
		}		
	    get=false;
	    i++;
	}
	newNode = new Node<TypeName>(NewEntry,i);  //note that the parent of the object is meaningless, 
	ptr->children.push_back(newNode);	       //cause there might be multiply data structure point to the object
	newNode=nullptr;
	ItemCount++;
}
template<typename TypeName>
Node<TypeName>* Bag<TypeName>::findNode(string& name){ //find the object
	bool get=false;
	Node<TypeName>* ptr = nullptr;       	
	for(int i=0;i<header.size();i++){                 //determine the first letter
		if(header[i]->key==name[0]){
			ptr = header[i];
			get=true;
			break;
		}		    
	}
	if(get==false)
		return nullptr;
	    
	get=false;
	int i=1;
	while(i<name.length()){
		for(int j=0;j<ptr->children.size();j++){
		    if(ptr->children[j]->key == name[i]){
				ptr = ptr->children[j];
		    	get=true;	    	
		    	break;
			}
		}
		if(get==false){
			return nullptr;
		}	    
		get=false;
		i++;
	}
	return ptr;
}
template<typename TypeName>
TypeName* Bag<TypeName>::search(string& name){
	Node<TypeName>* ptr=findNode(name);
    if(ptr==nullptr)
	    return nullptr; 
	return ptr->children[0]->object;
}
template<typename TypeName>
TypeName* Bag<TypeName>::remove(string& name) throw(logic_error){
	Node<TypeName>* ptr = findNode(name);
	if(ptr==nullptr)
	    throw logic_error("removing an non-exist item");
    
	//--------------find it ---------- ptr->children[0]->object
	TypeName* removeObject = ptr->children[0]->object;
	ptr->children.pop_back();
	while(ptr->children.size()==0 && ptr->parent!=nullptr){
		Node<TypeName>* par = ptr->parent;
		int length = par->children.size();
		for(int i=0;i<length;i++){
			if(par->children[i]->key==ptr->key){
				delete ptr;
				par->children.erase(par->children.begin()+i);
				break;
			}
		}
		ptr = par;	
	}
	ItemCount--;
	return removeObject;
}
template<typename TypeName>
bool Bag<TypeName>::isEmpty(){
	if(ItemCount==0)
	    return true;
	return false;
}
template<typename TypeName>
vector<TypeName*> Bag<TypeName>::depth_first_search(Node<TypeName>* p){ //traversal recursion
	Node<TypeName>* ptr = p;
	vector<TypeName*> subObject,temp;
	int length=p->children.size();
	for(int j=0;j<length;j++){
		ptr = p->children[j];
    	if(ptr->object!=nullptr){
    		subObject.push_back(ptr->object);
		}	    
    	else{
    		temp=depth_first_search(ptr);
    		for(int i=0;i<temp.size();i++)
    			subObject.push_back(temp[i]);
		}
	}	
	    
	return subObject;
}
template<typename TypeName>
vector<TypeName*> Bag<TypeName>::traversal(){
    vector<TypeName*> subObject,temp;
	for(int i=0;i<header.size();i++){
    	temp=depth_first_search(header[i]);  
		for(int i=0;i<temp.size();i++)
    		subObject.push_back(temp[i]);	
	}
	return subObject;
}
template<typename TypeName>
void Bag<TypeName>::clear(){
	vector<TypeName*> all = this->traversal();
	for(int i=0;i<all.size();i++)
		this->remove(all[i]->getName());
}


//--------------------global function----------------------------
matchUp* match(Car* driver, Passenger* caller, string& time,       
               int Max_dis, int idealScore, int tagScore, int disWeighted){
	driver->ChangeDir(time,'\0');
	int distance=0,tag=0,matchScore=0;
	distance=abs(driver->x_coordinate-caller->getX())+abs(driver->y_coordinate-caller->getY());
	if(distance<=Max_dis){
	    for(int i=0;i<driver->characteristic.size();i++){
	    	for(int j=0;j<caller->getTag().size();j++){
	    		if(driver->characteristic[i]==(caller->getTag())[j]){
	    			tag++;
	    			break;
				}
			}
		}
		matchScore=driver->score - (idealScore*driver->GetScoreCount) + (tagScore*tag) - (disWeighted*distance);
		matchUp* CandP = new matchUp(matchScore,distance,driver->order);
		driver->tagWithP=tag;
		return CandP;
	}

	return nullptr;
}
Car* applyCar(Bag<Car>& emptyLorR, Passenger* caller, string& time,
              int Max_dis, int idealScore, int tagScore, int disWeighted){
	vector<Car*> emptyCar;
	int matchScore=0,getCar=-1;
	bool get=false;
	matchUp* temp;
	matchUp* iWantThis;
	emptyCar = emptyLorR.traversal(); 
//	for(int i=0;i<emptyCar.size();i++)
//	    emptyCar[i]->print();
	for(int i=0;i<emptyCar.size();i++){
	    if(get==false){
	    	iWantThis = match(emptyCar[i],caller,time,Max_dis,idealScore,tagScore,disWeighted);
			if(iWantThis!=nullptr){
	    		getCar=i;
				get=true;
			}	    		
		}
		else{
			temp=match(emptyCar[i],caller,time,Max_dis,idealScore,tagScore,disWeighted);
			if(temp!=nullptr){
		    	if(*temp>*iWantThis){
		    		delete iWantThis;
		    		iWantThis=temp;
		    		getCar=i;
				}
		    	else
				    delete temp;
			}
		}	 	   	
	}
	if(getCar!=-1){
		 return emptyCar[getCar];		 
	}	   
	else
	    return nullptr;
}
satisfy grading(Passenger* caller, string& time, string& location, int tagCount, bool isRegular){
	
	char hour[3],minute[3];
	hour[0]=time[0];hour[1]=time[1];hour[2]='\0';
	minute[0]=time[3];minute[1]=time[4];minute[2]='\0';
	short h=0,min=0,arrivalTime=0;
	h=atoi(hour);
	min=atoi(minute);
	arrivalTime=h*60+min;
	
	string x,y;
	int x_co=0,y_co=0;
	location.pop_back();
	y=location.substr(location.find_last_of(",")+1);
	while(location[location.length()-1]!=',')
	    location.pop_back();
	location.pop_back();
	x=location.substr(location.find_last_of("(")+1);	
	x_co=stoi(x,nullptr,10);  //throw invalid_argument, out_of_range
	y_co=stoi(y,nullptr,10);
	
	int distance=0,copydis=0;
	short waitingTime=0,routeTime=0;
	satisfy p;
	p.score=4;
	waitingTime=caller->onboardTime - caller->onlineTime ;
	routeTime=arrivalTime - caller->onboardTime;
	distance = abs(x_co - caller->x_coordinate) + abs(y_co - caller->y_coordinate);
        copydis=distance;

	if(waitingTime>10 && waitingTime<=20)   //等待時間扣分 
    	p.score--;
    else if(waitingTime>20){
    	p.score -= 2;
    	p.money = -1;
	}

    if(isRegular==true){                    //載送時間扣分 
    	if(routeTime>distance*2 && routeTime<=distance*3)
    	    p.score--;
    	else if(routeTime>distance*3){
    		p.score -= 2;
    		p.money = -1;
		}	    
	} 
	else{
		copydis /= 2;
		if(routeTime>copydis*2 && routeTime<=copydis*3)
    	    p.score--;
    	else if(routeTime>copydis*3){
    		p.score -= 2;
    		p.money = -1;
		}	    
	}
	p.score += tagCount;     //標籤相同加分
	if(p.score>=5)
	    p.score=5;
	else if(p.score<=1)
	    p.score=1;
	p.distance=distance;
	return p; 
}
