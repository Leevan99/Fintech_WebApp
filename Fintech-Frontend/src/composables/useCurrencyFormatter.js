export function useCurrencyFormatter(locale = 'it-IT', currency = 'EUR') {
  const formatCurrency = (value) => {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency,
    }).format(value);
  };

  return { formatCurrency };
}
