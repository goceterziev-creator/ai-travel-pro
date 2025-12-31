# ... [всички imports и функции същите до PDF] ...

def create_aya_pdf(name, dest, total, flights, hotels, nights):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 180, 219)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, 'AYA AI TRAVEL BOOK V4', 0, 1, 'C')
    
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f'Client: {name}', 0, 1, 'C')
    pdf.cell(0, 10, f'Trip: {dest}', 0, 1, 'C')
    pdf.cell(0, 10, f'Total: EUR {total:.0f}', 0, 1, 'C')
    
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Flight: {flights["airline"].iloc[0]} EUR {flights["price"].iloc[0]}', 0, 1)
    pdf.cell(0, 10, f'Hotel: {hotels["name"].iloc[0]} EUR {hotels["price"].iloc[0]}/night x{nights}', 0, 1)
    
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f'{CONTACT_NAME}', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Email: {OFFICIAL_EMAIL}', 0, 1, 'C')
    pdf.cell(0, 10, f'Phone: +359 894 84 28 82', 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# ... [остановката на кода същата] ...
