from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MortgageCalculatorView(APIView):
    def post(self, request):
        try:
            price         = float(request.data.get('price'))
            down_payment  = float(request.data.get('down_payment', 0))
            interest_rate = float(request.data.get('interest_rate'))
            years         = int(request.data.get('years'))
        except (TypeError, ValueError):
            return Response(
                {'error': 'price, interest_rate aur years zaroori hain aur numbers hone chahiye'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if down_payment >= price:
            return Response(
                {'error': 'Down payment property price se kam honi chahiye'},
                status=status.HTTP_400_BAD_REQUEST
            )

        principal     = price - down_payment
        monthly_rate  = (interest_rate / 100) / 12
        n_payments    = years * 12

        if monthly_rate == 0:
            monthly_payment = principal / n_payments
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / \
                               ((1 + monthly_rate) ** n_payments - 1)

        total_payment  = monthly_payment * n_payments
        total_interest = total_payment - principal

        return Response({
            'property_price':   round(price, 2),
            'down_payment':     round(down_payment, 2),
            'loan_amount':      round(principal, 2),
            'interest_rate':    interest_rate,
            'loan_years':       years,
            'monthly_payment':  round(monthly_payment, 2),
            'total_payment':    round(total_payment, 2),
            'total_interest':   round(total_interest, 2),
        })