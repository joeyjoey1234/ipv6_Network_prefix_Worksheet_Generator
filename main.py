import random
from fpdf import FPDF
import ipaddress

# Function to generate a random IPv6 address within the real-life unicast range (2000::/3)
def generate_real_life_ipv6():
    # Global unicast addresses fall within 2000::/3 range (2000:: to 3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff)
    prefix_base = random.randint(0x2000, 0x3fff)  # Restrict to 2000::/3 range
    remaining_bits = random.getrandbits(112)  # 128 - 16 bits already used by the first part
    ipv6_address = ipaddress.IPv6Address((prefix_base << 112) | remaining_bits)
    prefix_length = random.randint(32, 64)  # Random prefix length for testing
    return ipv6_address, prefix_length

# Function to calculate the network prefix
def get_network_prefix(ipv6_address, prefix_length):
    network = ipaddress.IPv6Network(f"{ipv6_address}/{prefix_length}", strict=False)
    return str(network)

# Function to create a PDF with real-life random IPv6 addresses and answers at the end as an answer sheet
def create_pdf_with_real_life_ipv6(prefix_count=10, file_name="ipv6_test_with_answer_sheet.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="Real-Life IPv6 Network Prefix Test", ln=True, align="C")
    pdf.ln(10)

    # Instruction
    pdf.multi_cell(200, 10, txt="Instructions: For each IPv6 address and prefix length provided below, "
                                "find the network prefix. Use the space provided for your answer.")
    pdf.ln(5)

    # Store answers for the end
    answers = []

    # Generating random real-life prefixes with space for answers
    for i in range(prefix_count):
        ipv6_address, prefix_length = generate_real_life_ipv6()
        ipv6_prefix = f"{ipv6_address}/{prefix_length}"
        
        # Display the question
        pdf.cell(200, 10, txt=f"{i + 1}. Find the network prefix for the following IPv6 address:", ln=True)
        pdf.cell(200, 10, txt=f"   {ipv6_prefix}", ln=True)
        
        # Leave a gap for the answer and work
        pdf.ln(20)

        # Calculate the correct network prefix and store it
        network_prefix = get_network_prefix(ipv6_address, prefix_length)
        answers.append(f"{i + 1}. {ipv6_prefix} -> Network Prefix: {network_prefix}")

    # Add an answer sheet section at the very end
    pdf.add_page()
    pdf.cell(200, 10, txt="Answer Sheet", ln=True, align="C")
    pdf.ln(10)

    for answer in answers:
        pdf.multi_cell(200, 10, txt=answer)
        pdf.ln(5)

    # Save the PDF to the specified file
    pdf.output(file_name)
    print(f"PDF generated with {prefix_count} real-life IPv6 prefixes and an answer sheet at the end: {file_name}")

# Run the script
if __name__ == "__main__":
    create_pdf_with_real_life_ipv6(prefix_count=20)
