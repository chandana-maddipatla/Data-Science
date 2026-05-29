import org.junit.Test;

public class AppTest {

    @Test
    public void testEmployee() {

        Employee emp =
                new Employee(1, "Sai", "IT");

        emp.display();
    }
}
