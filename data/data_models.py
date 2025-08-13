from dataclasses import dataclass, field
from datetime import datetime
from typing import List,Optional

@dataclass
class Trade:
    trade_id: str
    symbol: str
    trade_type: str
    quantity: float
    price: float
    trade_date: datetime
    commission: float = 0.0
    notes: Optional[str] = None
    
@dataclass
class Investment:
    investment_id: str
    name: str
    asset_type: str
    current_price: float
    quantity_held: float
    purchase_date: Optional[datetime] = None
    purchase_price : Optional[float] =None
    notes:Optional[str] = None
    
@dataclass
class Portfolio:
    portfolio_id: str
    name:str
    trades: List[Trade] = field(default_factory = list)
    investments: List[Investment] = field(default_factory = list)
    created_date: datetime = field(default_factory= datetime.now)
    description :Optional[str] = None
    
    def add_trade(self,trade:Trade):
        self.trades.append(trade)

    def add_investment(self,investment: Investment):
        self.investments.append(investment)
    
    def total_value(self) -> float:
        return sum (inv.current_price * inv.quantity_held for inv in self.investments)
    
    def total_commission(self) -> float:
        return sum(trade.commission for trade in self.trades)